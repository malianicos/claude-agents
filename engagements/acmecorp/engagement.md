# BRIDGEFALL — AcmeCorp Engagement

## Target
- **Primary Domain:** acmecorp.com
- **Stack:** IIS / Windows Server / Active Directory
- **Scope:** Full-scope authorized penetration test
- **ROE:** Webb-signed, Clause 4.2

## Phases

| # | Phase | Lead | Status |
|---|-------|------|--------|
| 1 | OSINT & Passive Recon | Fury (field) | ✅ COMPLETE |
| 2 | Active Enumeration | Stark + Widow | ⏳ QUEUED |
| 3 | Exploitation & Initial Access | Widow + Vision | ⏳ QUEUED |
| 4 | Post-Exploitation & AD Attack | Stark | ⏳ QUEUED |
| 5 | Reporting & PFCD Assembly | Fury | ⏳ QUEUED |

## Kill Chain Hypothesis (Pre-Recon)
1. IIS misconfig or exposed management endpoint → initial foothold
2. Web app vuln (auth bypass, deserialization, SSRF) → webshell/reverse shell
3. Service account credential harvest → lateral movement
4. Kerberoasting / AS-REP roasting / ADCS abuse → domain privilege escalation
5. DCSync / Golden Ticket → domain dominance

## Loot Log
- Azure AD Tenant ID: `ea92efc7-efc6-4e52-877a-b08324464f69`
- M365 Verification: `MS=ms75953865`
- Staging environment: `acme.ooddademo.com` @ `67.203.23.68` (NO WAF)
- VPN gateway: `vpn.acmecorp.com` @ `64.77.238.117` (VTX Telecom)
- Origin IP candidates: `23.228.86.241`, `64.77.238.21`, `64.77.238.22`
- Sucuri WAF ID: 14017
- DMARC: p=none (spoofing viable)
- GraphQL endpoint: LIVE (HTTP 200)
- REST API: EXISTS (HTTP 401 — needs auth enum)
