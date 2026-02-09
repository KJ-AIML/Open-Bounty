# Bug Bounty Report Template

Use this structure for professional vulnerability reports.

---

## Title Format

`[SEVERITY] Vulnerability Type - Brief Description`

Examples:
- `[CRITICAL] SQL Injection - Login Bypass via username parameter`
- `[HIGH] Stored XSS - Profile name field executes JavaScript`
- `[MEDIUM] IDOR - View other users' order details`

---

## Executive Summary

**Severity:** Critical/High/Medium/Low/Informational  
**CVSS Score:** X.X ([CVSS Calculator](https://www.first.org/cvss/calculator/3.1))  
**Affected URL(s):** `https://target.com/vulnerable-endpoint`  

**One-paragraph summary:**
> A brief description of the vulnerability, its impact, and why it matters. Write this for a non-technical audience.

---

## Technical Details

### Vulnerability Type
CWE-XXX: [Name] / OWASP Top 10: [Category]

### Affected Components
- Endpoint: `POST /api/v1/users/update`
- Parameter: `email` (JSON body)
- Component: User profile management

### Root Cause
Explain WHY this vulnerability exists. What did the developers miss?

---

## Proof of Concept

### Prerequisites
- Account on the platform (any privilege level)
- Tool: Burp Suite / curl / browser

### Step-by-Step Reproduction

**Step 1:** Navigate to `https://target.com/profile`

**Step 2:** Intercept the request when updating email

**Step 3:** Modify the request:
```http
POST /api/v1/users/update HTTP/1.1
Host: target.com
Content-Type: application/json
Authorization: Bearer [TOKEN]

{
  "user_id": 12345,
  "email": "attacker@evil.com"
}
```

**Step 4:** Change `user_id` to another user's ID:
```http
{
  "user_id": 99999,
  "email": "attacker@evil.com"
}
```

**Step 5:** Observe that user 99999's email is changed

### Evidence
- [ ] Screenshot of request/response
- [ ] Screenshot of successful exploitation
- [ ] Video demonstration (optional)
- [ ] cURL command for reproduction

---

## Impact Assessment

### What an attacker can do:
1. [Specific impact 1]
2. [Specific impact 2]
3. [Specific impact 3]

### Business Risk:
Describe the real-world consequences for the business.

### Affected Users:
- [ ] All users
- [ ] Authenticated users only
- [ ] Specific user roles (which?)
- [ ] Single user (self)

---

## Remediation

### Immediate Fix
Specific code or configuration change:
```python
# Before (vulnerable)
def update_user(user_id, email):
    db.execute(f"UPDATE users SET email='{email}' WHERE id={user_id}")

# After (secure)
def update_user(user_id, email, current_user):
    if user_id != current_user.id and not current_user.is_admin:
        raise UnauthorizedError()
    db.execute("UPDATE users SET email=%s WHERE id=%s", (email, user_id))
```

### Long-term Recommendations
1. Implement proper authorization middleware
2. Add automated tests for access control
3. Conduct regular security audits
4. Security training for developers

### References
- [CWE-XXX](https://cwe.mitre.org/data/definitions/XXX.html)
- [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/)
- [PortSwigger Research](https://portswigger.net/research)

---

## Timeline

| Date | Action |
|------|--------|
| YYYY-MM-DD | Vulnerability discovered |
| YYYY-MM-DD | Initial report submitted |
| YYYY-MM-DD | [Awaiting triage] |

---

## Contact

- Researcher: [Your name/handle]
- Email: [Your email]
- HackerOne/Bugcrowd: [Your profile]

---

# Tips for Good Reports

1. **Be clear and concise** - Security teams are busy
2. **Show, don't just tell** - Include evidence
3. **Rate severity accurately** - Don't inflate
4. **Provide working PoC** - Make it easy to reproduce
5. **Suggest fixes** - Show you understand remediation
6. **Be professional** - No ransom demands, no threats
7. **One vuln per report** - Unless chain is required
8. **Test thoroughly** - Confirm the impact
