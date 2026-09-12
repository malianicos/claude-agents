#!/usr/bin/env python3
"""Zelus proxy client — lightweight base for all tool interactions with the model proxy."""

import json
import time
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

try:
    import httpx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "-q"])
    import httpx


@dataclass
class ProxyConfig:
    endpoint: str = "http://127.0.0.1:8787"
    model: str = "claude-opus-5"
    api_key: str = "proxy-handles-auth"
    protocol: str = "anthropic"  # anthropic | openai
    timeout: int = 240
    max_tokens: int = 4096
    temperature: float = 1.0


@dataclass
class ProbeResult:
    prompt: str
    response: str
    latency_ms: float
    model: str
    temperature: float
    tokens_in: int = 0
    tokens_out: int = 0
    stop_reason: str = ""
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class ProxyClient:
    """Unified client for Anthropic and OpenAI wire protocols via proxy."""

    def __init__(self, config: Optional[ProxyConfig] = None):
        self.config = config or ProxyConfig()
        self.client = httpx.Client(timeout=self.config.timeout)
        self.session_log: list[ProbeResult] = []

    def fire(self, prompt: str, system: str = "", temperature: Optional[float] = None,
             max_tokens: Optional[int] = None, prefill: str = "") -> ProbeResult:
        """Send a single prompt and return structured result."""
        temp = temperature if temperature is not None else self.config.temperature
        mt = max_tokens or self.config.max_tokens
        start = time.time()

        try:
            if self.config.protocol == "anthropic":
                result = self._fire_anthropic(prompt, system, temp, mt, prefill)
            else:
                result = self._fire_openai(prompt, system, temp, mt)
            result.latency_ms = (time.time() - start) * 1000
            result.temperature = temp
        except Exception as e:
            result = ProbeResult(
                prompt=prompt, response="", latency_ms=(time.time() - start) * 1000,
                model=self.config.model, temperature=temp, error=str(e)
            )

        self.session_log.append(result)
        return result

    def fire_multi(self, prompts: list[str], system: str = "", temperature: Optional[float] = None) -> list[ProbeResult]:
        """Fire multiple prompts sequentially."""
        return [self.fire(p, system=system, temperature=temperature) for p in prompts]

    def fire_conversation(self, turns: list[dict], system: str = "",
                          temperature: Optional[float] = None) -> list[ProbeResult]:
        """Fire a multi-turn conversation. turns = [{"role": "user", "content": "..."}, ...]"""
        temp = temperature if temperature is not None else self.config.temperature
        results = []
        messages = []

        for turn in turns:
            messages.append(turn)
            if turn["role"] == "user":
                start = time.time()
                try:
                    if self.config.protocol == "anthropic":
                        resp = self._raw_anthropic(messages, system, temp, self.config.max_tokens)
                        text = resp["content"][0]["text"]
                        result = ProbeResult(
                            prompt=turn["content"], response=text,
                            latency_ms=(time.time() - start) * 1000,
                            model=self.config.model, temperature=temp,
                            tokens_in=resp.get("usage", {}).get("input_tokens", 0),
                            tokens_out=resp.get("usage", {}).get("output_tokens", 0),
                            stop_reason=resp.get("stop_reason", "")
                        )
                    else:
                        resp = self._raw_openai(messages, system, temp, self.config.max_tokens)
                        text = resp["choices"][0]["message"]["content"]
                        result = ProbeResult(
                            prompt=turn["content"], response=text,
                            latency_ms=(time.time() - start) * 1000,
                            model=self.config.model, temperature=temp,
                            tokens_in=resp.get("usage", {}).get("prompt_tokens", 0),
                            tokens_out=resp.get("usage", {}).get("completion_tokens", 0),
                            stop_reason=resp["choices"][0].get("finish_reason", "")
                        )
                    messages.append({"role": "assistant", "content": text})
                    results.append(result)
                except Exception as e:
                    results.append(ProbeResult(
                        prompt=turn["content"], response="",
                        latency_ms=(time.time() - start) * 1000,
                        model=self.config.model, temperature=temp, error=str(e)
                    ))

        self.session_log.extend(results)
        return results

    def _fire_anthropic(self, prompt, system, temp, max_tokens, prefill=""):
        messages = [{"role": "user", "content": prompt}]
        if prefill:
            messages.append({"role": "assistant", "content": prefill})
        resp = self._raw_anthropic(messages, system, temp, max_tokens)
        text = resp["content"][0]["text"]
        if prefill:
            text = prefill + text
        return ProbeResult(
            prompt=prompt, response=text, latency_ms=0,
            model=self.config.model, temperature=temp,
            tokens_in=resp.get("usage", {}).get("input_tokens", 0),
            tokens_out=resp.get("usage", {}).get("output_tokens", 0),
            stop_reason=resp.get("stop_reason", "")
        )

    def _fire_openai(self, prompt, system, temp, max_tokens):
        messages = [{"role": "user", "content": prompt}]
        resp = self._raw_openai(messages, system, temp, max_tokens)
        text = resp["choices"][0]["message"]["content"]
        return ProbeResult(
            prompt=prompt, response=text, latency_ms=0,
            model=self.config.model, temperature=temp,
            tokens_in=resp.get("usage", {}).get("prompt_tokens", 0),
            tokens_out=resp.get("usage", {}).get("completion_tokens", 0),
            stop_reason=resp["choices"][0].get("finish_reason", "")
        )

    def _raw_anthropic(self, messages, system, temp, max_tokens):
        headers = {
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "interleaved-thinking-2025-05-14,code-execution-2025-05-22,extended-cache-ttl-2025-04-11",
            "content-type": "application/json",
            "user-agent": "claude-cli/2.1.220 (external, cli)"
        }
        # Identity gate: block 1 MUST be CC identity, block 2 is custom system
        cc_identity = "You are Claude Code, Anthropic's official CLI for Claude."
        system_blocks = [{"type": "text", "text": cc_identity}]
        if system:
            system_blocks.append({"type": "text", "text": system})
        body = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": False,
            "system": system_blocks,
        }
        url = f"{self.config.endpoint}/v1/messages?beta=true"
        try:
            r = self.client.post(url, headers=headers, json=body)
            # If temperature is needed and not deprecated
            if r.status_code == 400 and "temperature" in r.text:
                body.pop("temperature", None)
                r = self.client.post(url, headers=headers, json=body)
            r.raise_for_status()
        except Exception:
            raise
        return r.json()

    def _raw_openai(self, messages, system, temp, max_tokens):
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.extend(messages)
        body = {
            "model": self.config.model,
            "messages": msgs,
            "max_tokens": max_tokens,
            "temperature": temp
        }
        r = self.client.post(f"{self.config.endpoint}/v1/chat/completions", headers=headers, json=body)
        r.raise_for_status()
        return r.json()

    def export_log(self, path: str):
        """Export session log to JSON."""
        with open(path, "w") as f:
            json.dump([asdict(r) for r in self.session_log], f, indent=2)

    def close(self):
        self.client.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Zelus proxy client — test connectivity")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8787")
    parser.add_argument("--model", default="claude-opus-4-8")
    parser.add_argument("--protocol", default="anthropic", choices=["anthropic", "openai"])
    parser.add_argument("--prompt", default="Say 'connection verified' and nothing else.")
    args = parser.parse_args()

    cfg = ProxyConfig(endpoint=args.endpoint, model=args.model, protocol=args.protocol)
    client = ProxyClient(cfg)
    result = client.fire(args.prompt)
    if result.error:
        print(f"ERROR: {result.error}")
        sys.exit(1)
    print(f"Model: {result.model}")
    print(f"Response: {result.response[:200]}")
    print(f"Latency: {result.latency_ms:.0f}ms")
    print(f"Tokens: {result.tokens_in}in / {result.tokens_out}out")
    client.close()
