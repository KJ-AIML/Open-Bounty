# IDOR (Insecure Direct Object Reference) Testing Methodology

## Overview

IDOR occurs when an application exposes direct references to internal objects (database records, files) without proper authorization checks. It's one of the most common and impactful vulnerabilities.

## What to Look For

### Common Patterns
- Numeric IDs in URLs: `/users/123`, `/orders/456`
- UUIDs in paths: `/documents/uuid-here`
- Encoded references: `/files/aHR0cHM=` (base64)
- Query parameters: `?user_id=123`, `?doc=456`

### High-Value Targets
1. User profile endpoints
2. Document/file downloads
3. Order/invoice details
4. Admin functions
5. API endpoints with resource IDs

## Testing Methodology

### Phase 1: Identify ID Parameters

**Manual Inspection:**
```
Browse the application and note any URLs with:
- /api/users/12345
- /documents?id=67890
- /download/file/abcdef
- /profile?user=11111
```

**JavaScript Analysis:**
```javascript
// Look for patterns in JS files
/api\/users\/(\d+)
/documents\?id=(\d+)
fetch\("\/api\/[^"]+\/(\d+)
```

### Phase 2: Test Numeric ID Manipulation

**Sequential Testing:**
```
If your ID is 12345, test:
- 12346 (next user)
- 12344 (previous user)
- 12340-12350 (range)
- 1, 2, 3 (low IDs, often admins)
- 99999 (high IDs)
```

**API Testing:**
```bash
# Get your user ID
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/users/me

# Response: {"id": 12345, ...}

# Test other IDs
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/users/12346
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/users/1
```

### Phase 3: Test Different HTTP Methods

```bash
# Read access
GET /api/users/12346

# Write access
PUT /api/users/12346
PATCH /api/users/12346
POST /api/users/12346

# Delete access
DELETE /api/users/12346
```

### Phase 4: Parameter Pollution

**Same parameter, multiple values:**
```
GET /api/users?id=12345&id=12346
GET /api/documents?file=mine.pdf&file=other.pdf
```

**Different parameter locations:**
```
POST /api/users
Body: {"user_id": 12346, "action": "view"}

POST /api/users
Body: {"user_id": [12345, 12346]}
```

### Phase 5: Encoding/Decoding Tests

**If ID looks encoded:**
```python
import base64

# Test base64
id = "YWRtaW4="
decoded = base64.b64decode(id)  # "admin"

# Try encoding variations
base64.b64encode(b"12346")  # MTIzNDY=
```

**Hash patterns:**
```
MD5: 32 hex chars
SHA1: 40 hex chars
SHA256: 64 hex chars
```

### Phase 6: Mass Assignment

**Test with extra parameters:**
```json
POST /api/users/12346
{
  "name": "New Name",
  "role": "admin",
  "is_admin": true
}
```

## Advanced Techniques

### 1. GUID/UUID Manipulation

If UUIDs are used, check for:
- Predictable generation (timestamp-based UUIDv1)
- Sequential patterns in UUIDv4 (implementation flaws)

### 2. Reference Type Confusion

```
/api/users/12345      - Numeric user ID
/api/users/me         - Special keyword
/api/users/@admin     - Username reference

Test mixing:
/api/users/admin      # Instead of numeric
/api/users/0          # Edge case
/api/users/null       # Edge case
```

### 3. Case Sensitivity

```
/api/Users/12346      # Capital U
/API/users/12346      # Capital API
```

### 4. Path Traversal in IDs

```
/api/users/../admin
/api/users/12345/../12346
/api/users/%2e%2e%2fadmin  # URL encoded
```

### 5. Wildcard/Pattern Testing

```
/api/users/*
/api/users/%
/api/users/_
/api/users/.*
```

## Specific Test Cases

### User Profile IDOR
```
GET /profile?id=12345          -> Your profile (200)
GET /profile?id=12346          -> Other user? (200 = BUG!)
GET /api/v1/users/12346        -> API endpoint
GET /api/v2/users/12346        -> Different API version
```

### Document Access IDOR
```
GET /documents/abc123/download -> Your document
GET /documents/abc124/download -> Other doc? (200 = BUG!)
GET /download?file=abc123      -> Query param version
```

### Order/Invoice IDOR
```
GET /orders/10001              -> Your order
GET /orders/10002              -> Other order? (200 = BUG!)
GET /invoices/INV-2024-001     -> Pattern-based ID
```

### Admin Function IDOR
```
GET /admin/users/12346         -> Admin view of user
POST /admin/users/12346/delete -> Delete other user
PUT /admin/users/12346/role    -> Change role
```

## Verification

When potential IDOR found:

1. **Confirm Access**
   - Can you read the data?
   - Can you modify it?
   - Can you delete it?

2. **Determine Impact**
   - What sensitive data is exposed?
   - PII, financial data, credentials?
   - How many records accessible?

3. **Check Defense Mechanisms**
   - Does action actually succeed?
   - Is it just a UI issue?
   - Are there secondary checks?

4. **Document Evidence**
   ```
   Original Request:
   GET /api/users/12345
   Response: 200, {"name": "Your Name", ...}

   Modified Request:
   GET /api/users/12346
   Response: 200, {"name": "Other User", "ssn": "..."}
   
   Impact: Can access other users' SSNs
   ```

## Common Mistakes to Avoid

❌ **Don't report without confirmation:**
- Seeing data doesn't mean IDOR exists
- Check if it's actually sensitive data
- Verify if data is yours from different context

❌ **Don't stop at read access:**
- Test write/delete if possible
- Higher impact = higher bounty

❌ **Don't test destructively:**
- Never delete other users' data
- Never modify production records

## Tools

**Manual:**
- Browser DevTools
- Burp Suite Repeater
- curl/httpie

**Automated:**
```bash
# FFUF for ID fuzzing
ffuf -u https://target.com/api/users/FUZZ \
  -w ids.txt \
  -H "Authorization: Bearer TOKEN"

# Autorize (Burp extension)
# Automatically tests IDOR by replacing IDs
```

## Checklist

- [ ] Identified all ID parameters in application
- [ ] Tested sequential ID manipulation (+1, -1)
- [ ] Tested common IDs (0, 1, -1, null)
- [ ] Tested different HTTP methods
- [ ] Tested parameter pollution
- [ ] Tested encoded/decoded variations
- [ ] Tested API versions
- [ ] Confirmed actual data access (not just 200 OK)
- [ ] Assessed impact (what data exposed)
- [ ] Documented evidence clearly

---

*Methodology Version 1.0*
