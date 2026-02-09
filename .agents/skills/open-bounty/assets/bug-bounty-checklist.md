# Bug Bounty Target Checklist

Use this checklist when starting on a new target.

---

## Pre-Engagement

- [ ] Read program scope thoroughly
- [ ] Note out-of-scope domains/functionalities
- [ ] Check for special rules (rate limits, testing windows)
- [ ] Review previously disclosed reports
- [ ] Set up testing environment (VM, VPN if needed)

---

## Reconnaissance

### Subdomain Discovery
- [ ] amass enum -passive
- [ ] subfinder -all
- [ ] assetfinder
- [ ] crt.sh certificate transparency
- [ ] Compile unique list
- [ ] Probe for live hosts (httpx)

### Port Scanning
- [ ] Quick scan top 1000 ports
- [ ] Full port scan on interesting targets
- [ ] Service version detection
- [ ] Screenshot web services (aquatone/gowitness)

### Content Discovery
- [ ] Directory brute force (common.txt)
- [ ] Directory brute force (medium list on priority targets)
- [ ] File extension fuzzing (.php, .bak, .old, .zip)
- [ ] API endpoint discovery (/api/, /v1/, /graphql)
- [ ] JavaScript file enumeration

### Technology Detection
- [ ] Wappalyzer scan
- [ ] Nuclei tech detection
- [ ] Error page analysis
- [ ] Header analysis (Server, X-Powered-By)

---

## Automated Scanning

- [ ] Nuclei full scan
- [ ] Nuclei (critical/high severity only)
- [ ] Nikto scan (if allowed by scope)
- [ ] SSL/TLS scan (testssl.sh)
- [ ] CORS misconfiguration scan
- [ ] Security headers check

---

## Manual Testing

### Authentication
- [ ] Registration functionality
  - [ ] Duplicate registration
  - [ ] Weak validation
  - [ ] Overwrite existing account
- [ ] Login functionality
  - [ ] SQL injection
  - [ ] Authentication bypass
  - [ ] Brute force protection
- [ ] Password reset
  - [ ] Token predictability
  - [ ] Token expiration
  - [ ] Host header injection
- [ ] Session management
  - [ ] Session fixation
  - [ ] Session timeout
  - [ ] Concurrent sessions
- [ ] 2FA/MFA
  - [ ] Bypass possibilities
  - [ ] Brute force OTP
  - [ ] Backup codes handling

### Input Validation
- [ ] SQL Injection
  - [ ] URL parameters
  - [ ] POST body
  - [ ] Headers (User-Agent, Referer, X-Forwarded-For)
  - [ ] JSON/XML inputs
  - [ ] Search functionality
- [ ] XSS
  - [ ] Reflected XSS (all parameters)
  - [ ] Stored XSS (comments, profiles, messages)
  - [ ] DOM XSS (JavaScript sinks)
- [ ] Command Injection
- [ ] Path Traversal
  - [ ] File download functionality
  - [ ] File upload path manipulation
- [ ] XXE
  - [ ] XML upload/parsing
  - [ ] SOAP endpoints
  - [ ] DOCX/PDF/XML file uploads
- [ ] SSTI
  - [ ] Template rendering endpoints

### Access Control
- [ ] IDOR (Insecure Direct Object Reference)
  - [ ] Numeric ID manipulation
  - [ ] UUID manipulation
  - [ ] Hash/encoded ID manipulation
- [ ] Privilege Escalation
  - [ ] Horizontal (same role, different user)
  - [ ] Vertical (lower to higher role)
- [ ] Missing Authorization
  - [ ] Admin endpoints accessible
  - [ ] API endpoints without auth

### Business Logic
- [ ] Price manipulation
- [ ] Quantity manipulation (negative, decimal)
- [ ] Currency switching
- [ ] Workflow bypass
- [ ] Race conditions
- [ ] Time-based restrictions bypass

### File Operations
- [ ] File Upload
  - [ ] Extension bypass
  - [ ] Content-type bypass
  - [ ] Magic bytes bypass
  - [ ] Path traversal in filename
  - [ ] Size limit bypass
  - [ ] Malicious file types (SVG, HTML)
- [ ] File Download
  - [ ] Path traversal
  - [ ] SSRF via file download

### Client-Side
- [ ] CORS misconfiguration
- [ ] PostMessage vulnerabilities
- [ ] DOM manipulation issues
- [ ] LocalStorage/SessionStorage exposure
- [ ] Sensitive data in JavaScript

### API Testing
- [ ] REST API endpoints
- [ ] GraphQL introspection
- [ ] GraphQL batching
- [ ] WebSocket security
- [ ] API versioning issues
- [ ] Mass assignment

---

## Advanced Testing

- [ ] Subdomain takeover check
- [ ] Cloud storage misconfigurations (S3, GCS, Azure)
- [ ] Git repository exposure
- [ ] .env/config file exposure
- [ ] Backup file discovery
- [ ] DNS takeover possibilities
- [ ] SPF/DMARC/DKIM misconfigurations
- [ ] Email header injection
- [ ] Host header injection
- [ ] HTTP Request Smuggling
- [ ] Cache Poisoning
- [ ] Clickjacking

---

## Reporting

- [ ] Draft report with full reproduction
- [ ] CVSS score calculation
- [ ] Severity rating justification
- [ ] Impact demonstration
- [ ] Remediation suggestions
- [ ] Screenshots/video evidence
- [ ] Proof of concept code/commands
- [ ] Proofread and format
- [ ] Submit to platform
- [ ] Track triage status

---

## Notes Template

```markdown
# Target: [Name]
# Date: [YYYY-MM-DD]
# Scope: [In-scope domains]

## Interesting Findings
- 

## Endpoints to Test
- 

## Tech Stack
- 

## Potential Vulnerabilities
- 

## Report Drafts
- 

## Submitted Reports
- 
```
