# BRIDGEFALL — Phase 1 OSINT Report
## Target: acmecorp.com
**Classification:** ENGAGEMENT CONFIDENTIAL  
**Date:** 2026-09-29  
**Analyst:** Fury (field recon, Hawkeye unavailable)

---

## 🔴 CRITICAL FINDINGS — Quick Wins

### 1. Unprotected Staging Environment (CRITICAL)
- **Host:** `acme.ooddademo.com` → `67.203.23.68` (Colocation America)
- **Stack:** Identical Magento 2 instance — same CSP policy, same payment integrations, same Engintron/Nginx
- **WAF:** **NONE.** Production is behind Sucuri. Staging is bare.
- **Impact:** Full application attack surface without WAF interference. Likely shares database credentials, API keys, or admin accounts with production.
- **Confidence:** HIGH — confirmed via HTTP headers and CSP match

### 2. Azure AD User Enumeration (HIGH)
- **Tenant ID:** `ea92efc7-efc6-4e52-877a-b08324464f69`
- **Endpoint:** `login.microsoftonline.com` OAuth token endpoint
- **Behavior:** AADSTS50034 distinguishes "user does not exist" from valid accounts
- **Impact:** Build validated user list for password spray attacks against OWA/M365
- **Confidence:** HIGH — confirmed via live testing

### 3. DMARC Policy: None (HIGH)
- **Record:** `v=DMARC1; p=none`
- **Impact:** Email spoofing from @acmecorp.com is trivially achievable. Enables phishing campaigns impersonating executives for initial access.
- **Confidence:** HIGH — confirmed via DNS

### 4. Magento GraphQL Endpoint Exposed (MEDIUM-HIGH)
- **URL:** `https://www.acmecorp.com/graphql` → HTTP 200
- **Impact:** Magento 2 GraphQL APIs frequently expose customer data, product info, cart manipulation, and admin functionality when improperly configured
- **Confidence:** HIGH — endpoint confirmed live

### 5. Magento REST API Partial Access (MEDIUM)
- **URL:** `https://www.acmecorp.com/rest/V1/store/storeConfigs` → HTTP 401
- **Impact:** API exists and is authenticated (not 404). Other endpoints may be misconfigured with anonymous access.
- **Confidence:** MEDIUM — needs deeper enumeration

---

## 📡 Infrastructure Map

### DNS
| Record | Value | Notes |
|--------|-------|-------|
| NS | ns71.worldnic.com, ns72.worldnic.com | Network Solutions — legacy registrar |
| A | 192.124.249.168 | Sucuri WAF proxy |
| MX | acmecorp-com.mail.protection.outlook.com | Exchange Online |
| SPF | `v=spf1 mx:smtp.acmecorp.com ip4:23.228.86.241 ip4:104.223.136.79 ip4:64.77.238.21 ip4:64.77.238.22 include:spf.protection.outlook.com include:spf.mailjet.com ~all` | Multiple mail origins |
| DMARC | `v=DMARC1; p=none` | ⚠️ No enforcement |
| MS Verification | `MS=ms75953865` | M365 tenant confirmed |
| Google Verification | Present | Google services integration |

### Resolved Hosts
| Hostname | IP | Provider | Role |
|----------|-----|----------|------|
| www.acmecorp.com | 192.124.249.168 | Sucuri WAF | Production web (proxied) |
| mail.acmecorp.com | 104.223.136.79 | Amazon | Mail relay |
| vpn.acmecorp.com | 64.77.238.117 | VTX Telecom | VPN gateway |
| ftp.acmecorp.com | 50.62.160.39 | GoDaddy | FTP server |
| acme.ooddademo.com | 67.203.23.68 | Colocation America | **Staging (NO WAF)** |
| ooddademo.com | 107.179.19.93 | Amazon | Demo environment root |

### SPF-Disclosed Origin IPs (Mail Infrastructure)
| IP | Provider | Notes |
|----|----------|-------|
| 23.228.86.241 | Vault Host | Potential origin server |
| 104.223.136.79 | Amazon | Mail relay (= mail.acmecorp.com) |
| 64.77.238.21 | VTX Telecom | Same range as VPN — internal infra |
| 64.77.238.22 | VTX Telecom | Same range as VPN — internal infra |

### Microsoft 365 / Azure AD
| Property | Value |
|----------|-------|
| Tenant ID | `ea92efc7-efc6-4e52-877a-b08324464f69` |
| Exchange Online | ✅ (MX → mail.protection.outlook.com) |
| Autodiscover | → autodiscover.outlook.com |
| Skype/Teams | ✅ (SRV records: sipfed.online.lync.com, sipdir.online.lync.com) |
| Lync Discover | → webdir.online.lync.com |
| Enterprise Registration | → enterpriseregistration.windows.net (Azure AD Join) |
| Enterprise Enrollment | → enterpriseenrollment.manage.microsoft.com (Intune MDM) |
| User Enumeration | ⚠️ VULNERABLE via OAuth endpoint |

---

## 🏗️ Technology Stack

### ⚠️ STACK DISCREPANCY
**Client reported:** IIS on Windows Server  
**Observed externally:** Magento 2 on PHP 7.x/8.x + Nginx + Engintron (cPanel)  
**Assessment:** IIS likely runs internal services (SharePoint, ADFS, custom .NET apps). The public-facing e-commerce site is a Magento 2 deployment on Linux/cPanel infrastructure. Both may exist.

### Web Stack (Production)
| Layer | Technology |
|-------|-----------|
| WAF/CDN | Sucuri CloudProxy (ID: 14017) |
| Web Server | Nginx (behind Sucuri) |
| Reverse Proxy Cache | Engintron (cPanel Nginx integration) |
| Application | Magento 2 (PHP) |
| Session | PHPSESSID (PHP native sessions, 30min TTL) |
| Hosting Panel | cPanel (implied by Engintron) |

### Security Headers (Production)
| Header | Value | Grade |
|--------|-------|-------|
| HSTS | max-age=31536000; includeSubdomains; preload | ✅ Good |
| X-Frame-Options | SAMEORIGIN | ✅ Good |
| X-Content-Type-Options | nosniff | ✅ Good |
| X-XSS-Protection | 1; mode=block | ⚠️ Deprecated |
| CSP | Report-only mode | ⚠️ Not enforced |
| CSP default-src | 'self' 'unsafe-inline' 'unsafe-eval' | ❌ Weak |

### Payment Integrations (PCI Scope)
- PayPal (Payflow Link + Checkout)
- Braintree Gateway
- Cardinal Commerce (3D Secure)
- Amazon Pay (multi-region: US, UK, JP, IT, FR, ES, DE)
- Affirm (BNPL)
- Clover
- Google Pay

### Third-Party Services
- Adobe Analytics / DTM / Audience Manager (demdex.net)
- Google Analytics / Google Ads / GTM
- New Relic APM
- Microsoft Clarity
- Facebook Pixel / Connect
- Vimeo / YouTube embeds
- Signifyd (fraud protection)
- Mailjet (transactional email)
- reCAPTCHA

---

## 🎯 Attack Surface Summary

### Primary Attack Vectors (Prioritized)

1. **Staging Environment (acme.ooddademo.com)** — No WAF, full Magento instance. Test for:
   - Admin panel brute force
   - Magento RCE CVEs (Shoplift, Magento Killer, etc.)
   - GraphQL introspection + data exfiltration
   - REST API misconfigs
   - Default/shared credentials from production

2. **Azure AD Password Spray** — Enumerate valid users via AADSTS error codes, then spray common passwords against:
   - Outlook Web Access
   - Microsoft Teams
   - Azure Portal
   - Any ADFS/SSO endpoints

3. **Email Spoofing → Phishing** — DMARC p=none allows perfect spoofing. Craft executive impersonation phish to deliver:
   - OAuth consent phishing (Azure AD app consent)
   - Credential harvester (M365 login clone)
   - Macro-enabled document → reverse shell

4. **VPN Gateway (64.77.238.117)** — Identify VPN product and version. Check for:
   - Pulse Secure / Fortinet / Cisco AnyConnect vulns
   - Default credentials
   - Pre-auth RCE if outdated

5. **Magento GraphQL/REST API** — Production endpoints are live. Test for:
   - Introspection enabled
   - Unauthenticated queries (customer data, orders)
   - Cart/checkout manipulation
   - Admin mutation access

6. **Origin IP Discovery** — SPF IPs (23.228.86.241, 64.77.238.21-22) may host the real origin server. Direct access bypasses Sucuri WAF entirely.

7. **FTP Server (50.62.160.39)** — GoDaddy-hosted. Check for:
   - Anonymous access
   - Weak credentials
   - Sensitive file exposure

---

## 🔍 Intelligence Gaps (Phase 2 Requirements)

- [ ] crt.sh certificate transparency scan (browser required — direct API query)
- [ ] VPN product identification (requires active probing / banner grab)
- [ ] Employee email format and validated user list
- [ ] Internal hostname enumeration from cert SANs
- [ ] Shodan/Censys deep scan of all discovered IPs
- [ ] GitHub/GitLab code leak search for acmecorp
- [ ] Magento version fingerprinting on staging
- [ ] Full Magento admin path brute force on staging

---

## 📋 Recommended Phase 2 Dispatch

| Operator | Tasking |
|----------|---------|
| **Widow** | Magento exploitation on staging — admin brute force, GraphQL introspection, REST API enum, known CVE checks |
| **Stark** | Azure AD enumeration — user list build, password spray prep, VPN identification, network perimeter mapping of VTX Telecom range |
| **Strange** | Session/token analysis — PHPSESSID entropy, Magento CSRF tokens, OAuth flow weaknesses |
| **Vision** | Payload prep — Magento webshell, phishing templates, reverse shell for VPN/web exploitation |

---

*End of Phase 1 Report. Awaiting boss man's go/no-go for Phase 2 active enumeration.*
