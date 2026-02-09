---
name: open-bounty
description: Comprehensive bug bounty hunting and security assessment agent. Use when (1) User wants to test a website/application for security vulnerabilities, (2) User needs a vulnerability report drafted for submission, (3) User asks to find bugs, exploit, or assess security, (4) User needs help with reconnaissance, scanning, or analysis of targets, (5) User wants to claim rewards or help fix discovered issues.
---

# Open-Bounty: Bug Bounty Hunter

A comprehensive security assessment agent for finding vulnerabilities and creating actionable reports.

## Core Workflow

### Phase 1: Target Acquisition & Recon

```
1. Validate target scope and permissions
2. Gather target information (tech stack, subdomains, endpoints)
3. Build attack surface map
```

**Tech Stack Detection:**
- Wappalyzer, BuiltWith, or manual inspection
- Check headers, cookies, HTML comments
- JavaScript files analysis
- Error messages for version leaks

**Subdomain Enumeration:**
- amass, subfinder, assetfinder
- Certificate transparency logs (crt.sh)
- DNS bruteforce (gobuster dns)
- Permutation scanning (dnsgen + massdns)

### Phase 2: Vulnerability Scanning

**Automated Scanning:**
- nuclei (comprehensive vulnerability scanner)
- nmap (port and service detection)
- ffuf/gobuster (directory/file fuzzing)
- sqlmap (SQL injection testing)
- dalfox (XSS detection)

**Manual Testing Priorities:**
See [references/vuln-types.md](references/vuln-types.md) for detailed testing guides on:
- SQL Injection
- XSS (Reflected, Stored, DOM)
- CSRF/SSRF
- Authentication bypasses
- IDOR (Insecure Direct Object Reference)
- Business logic flaws
- Information disclosure

### Phase 3: Exploitation & Validation

**Rules of Engagement:**
- NEVER exploit without permission
- Use proof-of-concept only (no data exfiltration)
- Stop at first successful exploitation
- Document exact reproduction steps

**PoC Creation:**
- Minimal reproducible exploit
- Screenshots/video evidence
- Impact demonstration (without harm)

### Phase 4: Report Generation

Use [references/report-template.md](references/report-template.md) for structure:

```markdown
# Executive Summary
- Severity rating (CVSS score)
- One-paragraph impact description

# Technical Details
- Vulnerability type
- Affected endpoint/parameter
- Root cause analysis

# Proof of Concept
- Step-by-step reproduction
- Request/response samples
- Evidence (screenshots, videos)

# Impact Assessment
- What attacker can achieve
- Business risk

# Remediation
- Specific fix recommendations
- Code examples if applicable
- References (CWE, OWASP)
```

## Quick Reference Commands

### Subdomain Enumeration
```bash
# Amass
amass enum -passive -d target.com -o subs.txt

# Subfinder
subfinder -d target.com -all -o subs.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%.target.com&output=json" | jq -r '.[].name_value' | sort -u
```

### Port Scanning
```bash
# Quick nmap
nmap -sV -sC -O -oN nmap-quick.txt target.com

# Full port scan
nmap -p- -sV -oN nmap-full.txt target.com

# Nuclei scan
nuclei -u https://target.com -o nuclei-results.txt
```

### Content Discovery
```bash
# Directory fuzzing
gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o dirs.txt

# FFUF (fast)
ffuf -u https://target.com/FUZZ -w wordlist.txt -o ffuf-results.json
```

### Web Vuln Scanning
```bash
# SQLMap
sqlmap -u "https://target.com/page?id=1" --batch --level=3 --risk=2

# Dalfox (XSS)
dalfox url "https://target.com/search?q=test" -o xss-results.txt

# GF + nuclei patterns
cat urls.txt | gf xss | nuclei -t xss-templates/
```

## Severity Ratings

| Severity | CVSS | Reward Range | Response Time |
|----------|------|--------------|---------------|
| Critical | 9.0-10.0 | $$$$ | Immediate |
| High | 7.0-8.9 | $$$ | 24-48h |
| Medium | 4.0-6.9 | $$ | 1-2 weeks |
| Low | 0.1-3.9 | $ | 2-4 weeks |
| Informational | 0 | - | Best effort |

## Bug Bounty Platforms

- **HackerOne** (hackerone.com) - Largest platform
- **Bugcrowd** (bugcrowd.com) - Enterprise focus
- **Intigriti** (intigriti.com) - European focus
- **YesWeHack** (yeswehack.com) - European
- **Open Bug Bounty** (openbugbounty.org) - Responsible disclosure

## Important: Ethics & Legal

**ALWAYS:**
- Read and follow the program's scope/rules
- Stop testing if asked
- Report vulnerabilities promptly
- Keep findings confidential until fixed

**NEVER:**
- Test without authorization
- Exfiltrate sensitive data
- Cause denial of service
- Share vulnerabilities with others

## Resources

- [references/vuln-types.md](references/vuln-types.md) - Detailed vulnerability guides
- [references/report-template.md](references/report-template.md) - Report structure
- [references/methodology.md](references/methodology.md) - Testing methodology
- [references/tools.md](references/tools.md) - Tool recommendations
