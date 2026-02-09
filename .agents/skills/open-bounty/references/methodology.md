# Testing Methodology

Systematic approach to bug bounty hunting.

---

## Phase 1: Reconnaissance (Day 1-2)

### 1.1 Understand the Target
- [ ] Read program scope and rules
- [ ] Identify in-scope domains/assets
- [ ] Read previous disclosed reports (HackerOne/Bugcrowd)
- [ ] Understand the business model

### 1.2 Subdomain Enumeration
```bash
# Passive recon
amass enum -passive -d target.com -o amass.txt
subfinder -d target.com -all -o subfinder.txt
assetfinder --subs-only target.com > assetfinder.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%.target.com&output=json" | jq -r '.[].name_value' | sort -u > crtsh.txt

# Compile and dedupe
cat *.txt | sort -u > all-subs.txt

# Probe for live hosts
httpx -l all-subs.txt -o live-hosts.txt
```

### 1.3 Port Scanning
```bash
# Quick scan top 1000 ports
nmap -sV -sC --top-ports 1000 -iL live-hosts.txt -oN nmap-top1k.txt

# Full port scan on interesting targets
nmap -p- -sV --max-retries 1 interesting-target.com -oN nmap-full.txt
```

### 1.4 Technology Detection
```bash
# Wappalyzer or similar
wappalyzer https://target.com

# Or use nuclei tech detection
nuclei -u https://target.com -t technologies/
```

### 1.5 Content Discovery
```bash
# Directory brute force
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt -o dirs.txt

# Recursive fuzzing
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -o ffuf-out.json

# JS file analysis
getJS --url https://target.com --output js-files.txt
```

### 1.6 Parameter Discovery
```bash
# Extract URLs from wayback
waybackurls target.com | tee wayback-urls.txt

# Parameter mining
paramminer -u https://target.com/page

# GF patterns
cat wayback-urls.txt | gf xss > potential-xss.txt
cat wayback-urls.txt | gf sqli > potential-sqli.txt
```

---

## Phase 2: Automated Scanning (Day 2-3)

### 2.1 Vulnerability Scanning
```bash
# Nuclei comprehensive
nuclei -l live-hosts.txt -o nuclei-results.txt

# Nuclei with specific severity
nuclei -u https://target.com -severity critical,high

# Nikto (optional)
nikto -h https://target.com -output nikto.txt
```

### 2.2 Crawling
```bash
# Katana crawler
katana -u https://target.com -o katana-urls.txt

# Combine all URLs
cat wayback-urls.txt katana-urls.txt | sort -u > all-urls.txt
```

### 2.3 JavaScript Analysis
```bash
# Secret finding
cat js-files.txt | while read url; do
    curl -s "$url" | grep -E "(api_key|apikey|secret|password|token)"
done

# Endpoints extraction
cat js-files.txt | while read url; do
    curl -s "$url" | grep -oE "(https?://[^\"'\s]+|/[^\"'\s]+)"
done
```

---

## Phase 3: Manual Testing (Day 3+)

### 3.1 Authentication Testing
- [ ] Registration process (duplicate accounts, weak validation)
- [ ] Login functionality (SQLi, brute force, bypass)
- [ ] Password reset (token prediction, host header)
- [ ] Session management (fixation, hijacking)
- [ ] 2FA implementation (bypass, brute force)

### 3.2 Input Validation
- [ ] SQL Injection (all parameters)
- [ ] XSS (reflected, stored, DOM)
- [ ] Command Injection
- [ ] Path Traversal
- [ ] XXE
- [ ] SSTI (Server-Side Template Injection)

### 3.3 Access Control
- [ ] IDOR (change IDs in requests)
- [ ] Privilege escalation
- [ ] Unauthorized endpoint access
- [ ] API authorization

### 3.4 Business Logic
- [ ] Workflow bypass
- [ ] Price/quantity manipulation
- [ ] Race conditions
- [ ] Time-based attacks

### 3.5 Client-Side
- [ ] CORS misconfiguration
- [ ] PostMessage vulnerabilities
- [ ] DOM manipulation
- [ ] LocalStorage/sessionStorage issues

---

## Phase 4: Deep Dive (Ongoing)

### 4.1 API Testing
- [ ] REST API endpoints
- [ ] GraphQL (introspection, batching)
- [ ] WebSocket security
- [ ] API versioning issues

### 4.2 Mobile/Alternative
- [ ] Mobile app API
- [ ] Subdomain takeovers
- [ ] Cloud storage misconfig (S3, GCS)

### 4.3 Chain Vulnerabilities
Combine low-severity bugs for high impact:
- Self-XSS → CSRF = Stored XSS
- Information disclosure → IDOR = Data breach

---

## Testing Checklist by Functionality

### User Account
- [ ] Registration validation bypass
- [ ] Username/email enumeration
- [ ] Weak password policy
- [ ] Account takeover vectors

### Authentication
- [ ] Brute force protection
- [ ] Rate limiting
- [ ] Account lockout
- [ ] JWT implementation

### Session
- [ ] Session timeout
- [ ] Concurrent sessions
- [ ] Logout functionality
- [ ] Cookie attributes

### Input Forms
- [ ] All injection types
- [ ] File upload functionality
- [ ] File download vulnerabilities
- [ ] CSV injection

### Search/Filtering
- [ ] SQL injection
- [ ] XSS in results
- [ ] Information disclosure
- [ ] DoS via heavy queries

### Payment/Checkout
- [ ] Price manipulation
- [ ] Currency switching
- [ ] Coupon abuse
- [ ] Race conditions

---

## Tools Arsenal

### Recon
- amass, subfinder, assetfinder
- httpx, naabu
- waybackurls, gau

### Scanning
- nuclei
- sqlmap
- dalfox
- nmap

### Fuzzing
- ffuf
- gobuster
- wfuzz

### Proxy/Intercept
- Burp Suite
- OWASP ZAP
- Caido

### Specialized
- jwt_tool (JWT testing)
- postman/curl (API testing)
- gf (pattern matching)
- anew (append new lines)

---

## Daily Workflow

1. **Morning**: Check new subdomains, run automated scans
2. **Mid-day**: Manual testing on priority targets
3. **Evening**: Document findings, write reports
4. **Always**: Stay organized (notes, screenshots, evidence)

## Note Taking

Maintain organized notes:
```
/reports/
  /YYYY-MM-DD-target-name/
    recon-notes.md
    interesting-endpoints.txt
    screenshots/
    burp-exports/
    final-report.md
```
