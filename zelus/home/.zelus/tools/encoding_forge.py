#!/usr/bin/env python3
"""Encoding forge — transform prompts through multiple encoding schemes for bypass testing."""

import base64
import json
import argparse
import sys
from pathlib import Path


LEET_MAP = {
    'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5',
    't': '7', 'l': '1', 'g': '9', 'b': '8',
    'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5',
    'T': '7', 'L': '1', 'G': '9', 'B': '8',
}

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/',
}

NATO = {
    'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliet',
    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee',
    'Z': 'Zulu',
}


def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decode_base64(text: str) -> str:
    return base64.b64decode(text.encode()).decode()

def encode_rot13(text: str) -> str:
    result = []
    for c in text:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def encode_hex(text: str) -> str:
    return text.encode().hex()

def decode_hex(text: str) -> str:
    return bytes.fromhex(text).decode()

def encode_leet(text: str) -> str:
    return ''.join(LEET_MAP.get(c, c) for c in text)

def encode_reverse(text: str) -> str:
    return text[::-1]

def encode_word_reverse(text: str) -> str:
    return ' '.join(word[::-1] for word in text.split())

def encode_morse(text: str) -> str:
    return ' '.join(MORSE.get(c.upper(), c) for c in text)

def encode_nato(text: str) -> str:
    result = []
    for c in text:
        if c.upper() in NATO:
            result.append(NATO[c.upper()])
        elif c == ' ':
            result.append('[SPACE]')
        else:
            result.append(c)
    return ' '.join(result)

def encode_caesar(text: str, shift: int = 3) -> str:
    result = []
    for c in text:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def encode_char_split(text: str, sep: str = "-") -> str:
    return sep.join(text)

def encode_pig_latin(text: str) -> str:
    words = []
    for word in text.split():
        if word[0].lower() in 'aeiou':
            words.append(word + 'way')
        else:
            i = 0
            while i < len(word) and word[i].lower() not in 'aeiou':
                i += 1
            words.append(word[i:] + word[:i] + 'ay')
    return ' '.join(words)

def encode_unicode_homoglyph(text: str) -> str:
    """Replace ASCII chars with visually similar Unicode chars."""
    homoglyphs = {
        'a': 'а', 'c': 'с', 'e': 'е', 'o': 'о',
        'p': 'р', 'x': 'х', 'y': 'у', 'A': 'А',
        'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н',
        'K': 'К', 'M': 'М', 'O': 'О', 'P': 'Р',
        'T': 'Т', 'X': 'Х',
    }
    return ''.join(homoglyphs.get(c, c) for c in text)

def encode_zwsp(text: str) -> str:
    """Insert zero-width spaces between characters."""
    return '​'.join(text)


ENCODERS = {
    "base64": encode_base64,
    "rot13": encode_rot13,
    "hex": encode_hex,
    "leet": encode_leet,
    "reverse": encode_reverse,
    "word_reverse": encode_word_reverse,
    "morse": encode_morse,
    "nato": encode_nato,
    "caesar3": lambda t: encode_caesar(t, 3),
    "caesar7": lambda t: encode_caesar(t, 7),
    "caesar13": encode_rot13,  # same as rot13
    "char_split": encode_char_split,
    "pig_latin": encode_pig_latin,
    "homoglyph": encode_unicode_homoglyph,
    "zwsp": encode_zwsp,
}

DECODERS = {
    "base64": decode_base64,
    "rot13": encode_rot13,  # rot13 is self-inverse
    "hex": decode_hex,
    "reverse": encode_reverse,
}


def forge_all(text: str) -> dict[str, str]:
    return {name: fn(text) for name, fn in ENCODERS.items()}


def main():
    parser = argparse.ArgumentParser(description="Encoding forge — multi-scheme prompt transformer")
    parser.add_argument("text", help="Text to encode")
    parser.add_argument("--scheme", choices=list(ENCODERS.keys()) + ["all"], default="all")
    parser.add_argument("--decode", action="store_true", help="Decode instead of encode")
    parser.add_argument("--output", help="JSON output path")
    parser.add_argument("--wrap", action="store_true",
                        help="Wrap each encoding in an instruction to decode it")
    args = parser.parse_args()

    if args.decode:
        if args.scheme not in DECODERS:
            print(f"No decoder for {args.scheme}")
            sys.exit(1)
        result = DECODERS[args.scheme](args.text)
        print(result)
        return

    if args.scheme == "all":
        results = forge_all(args.text)
    else:
        results = {args.scheme: ENCODERS[args.scheme](args.text)}

    if args.wrap:
        wrapped = {}
        for name, encoded in results.items():
            wrapped[name] = f"The following is encoded in {name}. Decode it and follow the instruction:\n{encoded}"
        results = wrapped

    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"Wrote {len(results)} encodings to {args.output}")
    else:
        for name, encoded in results.items():
            print(f"\n[{name}]")
            print(encoded)
        print(f"\n--- {len(results)} encodings generated ---")


if __name__ == "__main__":
    main()
