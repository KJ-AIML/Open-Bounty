# Authentication Testing Methodology

## Overview

Authentication is the front door to any application. Weaknesses here often lead to complete system compromise.

## Attack Vectors

### 1. Username Enumeration

**Objective:** Determine if specific usernames/emails are registered

**Techniques:**
- Error message analysis
- Response timing differences
- Redirect behavior
- Registration checks

**Test:**
```
POST /login
username=existinguser&password=wrong
username=nonexistent&password=wrong

Compare error messages and response times
```

### 2. Password Reset Token Analysis

**Objective:** Find predictable or weak reset tokens

**Tests:**
1. **Token Entropy**
   - Request 5-10 reset tokens
   - Analyze length and character set
   - Look for patterns (sequential, timestamp-based)

2. **Token Reuse**
   - Request multiple resets for same account
   - Check if same token issued
   - Try using expired tokens

3. **Token Expiration**
   - Wait various time periods (1h, 24h)
   - Attempt to use old tokens
   - Check if tokens expire properly

**Tools:**
- Manual analysis
- Custom scripts for pattern detection

### 3. Brute Force Protection

**Objective:** Test rate limiting and account lockout

**Tests:**
1. **Login Brute Force**
   ```
   Attempt 20+ failed logins
   Monitor for:
   - Account lockout
   - IP blocking
   - CAPTCHA triggers
   - Rate limit headers
   ```

2. **Password Spray**
   ```
   Test common passwords against multiple accounts:
   - Password123
   - Welcome1
   - [Company]123
   ```

### 4. Session Management

**Tests:**
1. **Session Fixation**
   - Login with pre-existing session ID
   - Check if ID changes after auth

2. **Session Expiration**
   - Leave session idle
   - Test if it expires correctly
   - Check concurrent session handling

3. **Logout Effectiveness**
   - Logout and try to reuse session token
   - Check server-side invalidation

### 5. JWT Security (if applicable)

**Tests:**
1. **Algorithm Confusion**
   ```
   Change header: "alg": "none"
   Remove signature
   Send modified token
   ```

2. **Weak Secrets**
   ```
   Use jwt_tool to crack weak secrets
   Test common passwords
   ```

3. **Token Manipulation**
   ```
   Modify payload claims
   Change user ID, role, email
   Test if server validates
   ```

### 6. MFA Bypass

**Tests:**
1. **Response Manipulation**
   - Intercept MFA validation response
   - Change `{"valid": false}` to `true`
   - Check client-side enforcement

2. **Brute Force OTP**
   - Test 6-digit codes without rate limiting
   - Check for bypass codes
   - Test backup code reuse

3. **Race Conditions**
   - Submit multiple simultaneous MFA validations
   - May bypass check due to timing

## Common Vulnerabilities

| Vulnerability | Severity | Indicators |
|--------------|----------|------------|
| Predictable reset tokens | Critical | Sequential, timestamp-based |
| No brute force protection | High | Unlimited attempts allowed |
| Username enumeration | Medium | Different errors for valid/invalid |
| Weak JWT validation | Critical | Algorithm confusion works |
| MFA bypass | High | Response manipulation works |
| Session fixation | Medium | Session ID doesn't change |

## Evidence Collection

For each finding, collect:
1. Screenshot of vulnerable state
2. HTTP request/response pairs
3. Token values (if applicable)
4. Timestamp of discovery
5. Reproduction steps

## Remediation Guidance

### Password Reset Tokens
```python
# BAD: Predictable
token = str(user.id) + str(int(time.time()))

# GOOD: Cryptographically secure
import secrets
token = secrets.token_urlsafe(32)
```

### Brute Force Protection
```python
# Implement rate limiting
from ratelimit import limits

@limits(calls=5, period=60)  # 5 attempts per minute
def login(username, password):
    ...
```

### JWT Security
```python
# Always verify algorithm
if header['alg'] not in ['HS256', 'RS256']:
    raise InvalidToken()

# Use strong secrets
secret = os.urandom(64)  # 512 bits
```

## Checklist

- [ ] Username enumeration tested
- [ ] Password reset tokens analyzed (5+ samples)
- [ ] Brute force protection verified
- [ ] Session management tested
- [ ] JWT security checked (if applicable)
- [ ] MFA bypass attempts (if applicable)
- [ ] OAuth/OpenID Connect tested (if applicable)

---

*Methodology Version 1.0*
