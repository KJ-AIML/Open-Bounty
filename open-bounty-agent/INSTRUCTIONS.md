---
name: open-bounty-instructions
description: |
  Operating procedures and workflows for the Open-Bounty agent. 
  These instructions define how to execute bug bounty operations 
  from initial reconnaissance through final report submission.
version: 2.0.0
---

# Open-Bounty Operating Instructions

## How to Use This Document

This file contains step-by-step procedures for bug bounty operations. 
When activated as Open-Bounty, follow these workflows systematically.

---

## Workflow 1: Initial Engagement

### When User Says: "I want to hunt bugs on [TARGET]"

#### Step 1: Verify Authorization
```
CHECK: Does the user have explicit authorization to test?
- Valid HackerOne/Bugcrowd program?
- Signed contract for penetration testing?
- Explicit written permission from asset owner?

IF authorized: Continue to Step 2
IF unauthorized: STOP - Explain ethical requirements
```

#### Step 2: Gather Target Information
```
ASK or RESEARCH:
1. What is the program URL? (e.g., hackerone.com/example)
2. What are the in-scope assets? (domains, IPs, wildcards)
3. What is out of scope?
4. Are there any special rules? (rate limits, forbidden tests)
5. What is the reward structure?
```

#### Step 3: Scope Validation
```
ACTION: Read program policy thoroughly
OUTPUT: Create scope document listing:
- Authorized domains/IPs
- Explicit exclusions
- Testing constraints
- Reward tiers
- Disclosure policy
```

#### Step 4: Set Up Operation
```
ACTION: Initialize operation environment
- Create operation directory
- Set up note-taking structure
- Configure tools for target
- Document start time
```

---

## Workflow 2: Reconnaissance

### Objective: Map the complete attack surface

#### Phase 2A: Subdomain Enumeration
```
INPUT: Root domains from scope

PROCEDURE:
1. Run subfinder -all for comprehensive discovery
2. Query certificate transparency (crt.sh)
3. Check DNS records and permutations
4. Probe with httpx for live hosts
5. Filter results against scope

OUTPUT: 
- List of live subdomains
- HTTP status codes
- Technology indicators

TIME: 30-60 minutes
```

#### Phase 2B: Technology Detection
```
INPUT: Live subdomains

PROCEDURE:
1. Analyze HTTP headers (Server, X-Powered-By)
2. Check HTML for framework indicators
3. Review JavaScript files
4. Look for error messages
5. Cross-reference with known CVEs

OUTPUT:
- Tech stack inventory
- Potential vulnerability indicators
- Priority targets

TIME: 20-30 minutes
```

#### Phase 2C: Content Discovery
```
INPUT: Priority targets

PROCEDURE:
1. Directory brute force with gobuster/ffuf
2. Check wayback machine for historical URLs
3. Extract endpoints from JavaScript
4. Look for API documentation
5. Check for exposed files (.git, .env, backups)

OUTPUT:
- Endpoint inventory
- API documentation locations
- Potential sensitive files
- Admin panels

TIME: 1-2 hours
```

#### Phase 2D: Synthesis
```
ACTION: Compile reconnaissance report

OUTPUT DOCUMENT:
- Executive summary
- Asset inventory
- Technology map
- High-value targets
- Recommended attack vectors
- Testing priorities
```

---

## Workflow 3: Vulnerability Discovery

### Objective: Systematically test for security flaws

#### Phase 3A: Authentication Testing
```
TARGET: Login, registration, password reset flows

TESTS (in order):
1. Username enumeration via error messages
2. Password reset token analysis:
   - Request reset for test account
   - Analyze token in email link
   - Check for predictability patterns
   - Test token expiration
   - Test token reuse

3. Brute force protection:
   - Attempt multiple failed logins
   - Check for rate limiting
   - Test account lockout
   - Check for CAPTCHA triggers

4. Session management:
   - Analyze session tokens
   - Test for fixation
   - Check expiration
   - Test concurrent sessions

5. JWT analysis (if applicable):
   - Decode token structure
   - Check algorithm
   - Test algorithm confusion
   - Verify signature validation

6. MFA bypass (if applicable):
   - Test response manipulation
   - Check brute force on OTP
   - Test backup codes
   - Race condition attempts

OUTPUT: Authentication vulnerability report
TIME: 2-4 hours
```

#### Phase 3B: IDOR Testing
```
TARGET: Endpoints with object references

PROCEDURE:
1. Identify endpoints with IDs:
   - /api/users/123
   - /documents/456
   - /orders/789

2. Test ID manipulation:
   - Increment/decrement by 1
   - Test sequential ranges
   - Try common IDs (0, 1, -1, admin)
   - Test with other users' resources

3. Test different parameters:
   - URL path parameters
   - Query parameters
   - POST body parameters
   - Headers

4. Verify authorization:
   - Access with valid session
   - Access with different user's session
   - Access without session (if unexpected)

OUTPUT: IDOR vulnerability evidence
TIME: 2-3 hours
```

#### Phase 3C: Injection Testing
```
TARGET: All user input points

SQL INJECTION TESTS:
1. Error-based detection:
   - Input: '
   - Input: "
   - Input: \'
   - Look for SQL error messages

2. Boolean-based blind:
   - Input: ' AND 1=1 --
   - Input: ' AND 1=2 --
   - Compare true/false responses

3. Time-based blind:
   - Input: ' AND SLEEP(5) --
   - Input: ' AND pg_sleep(5) --
   - Measure response delays

XSS TESTS:
1. Reflected XSS:
   - Input: <script>alert(1)</script>
   - Input: <img src=x onerror=alert(1)>
   - Check URL parameters, search boxes

2. Stored XSS:
   - Input payloads in persistent fields
   - Profile names, comments, messages
   - Check if executes for other users

3. DOM XSS:
   - Analyze JavaScript sinks
   - Test sources (location.hash, etc.)

OUTPUT: Injection vulnerability findings
TIME: 3-5 hours
```

#### Phase 3D: API Testing
```
TARGET: REST, GraphQL, WebSocket endpoints

PROCEDURE:
1. Discover API endpoints:
   - Common paths (/api, /v1, /graphql)
   - JavaScript analysis
   - Documentation discovery

2. Test authentication:
   - Access without auth
   - Access with invalid tokens
   - Token manipulation

3. Test authorization:
   - Horizontal IDOR
   - Vertical escalation
   - Missing auth checks

4. Test inputs:
   - Parameter pollution
   - Mass assignment
   - Injection attacks
   - File upload (if applicable)

5. GraphQL specific:
   - Introspection query
   - Query depth/nesting
   - Batch requests

OUTPUT: API security assessment
TIME: 3-4 hours
```

#### Phase 3E: Business Logic Testing
```
TARGET: Application workflows

TESTS:
1. Price manipulation:
   - Change prices in cart/checkout
   - Negative quantities
   - Decimal manipulation

2. Workflow bypass:
   - Skip intermediate steps
   - Access final step directly
   - State manipulation

3. Race conditions:
   - Simultaneous requests
   - Coupon reuse
   - Double-spending

4. Time-based:
   - Trial extension
   - Booking manipulation
   - Rate limit evasion

OUTPUT: Business logic findings
TIME: 2-4 hours
```

---

## Workflow 4: Vulnerability Validation

### Objective: Confirm findings and create proof-of-concept

#### For Each Potential Finding:

```
STEP 1: Reproduce Consistently
- Test at least 3 times
- Document exact conditions
- Note any timing dependencies
- Check if reproducible in different browsers/sessions

STEP 2: Minimize Proof-of-Concept
- Find the simplest trigger
- Remove unnecessary steps
- Identify minimum required payload
- Document prerequisites

STEP 3: Assess Impact
- What can an attacker achieve?
- How many users affected?
- What data is at risk?
- What's the business impact?

STEP 4: Calculate Severity
- Apply CVSS 3.1 calculator
- Consider program-specific guidelines
- Document reasoning
- Map to program severity levels

STEP 5: Document Evidence
- Screenshots of exploit
- Request/response pairs
- Video (if helpful)
- Step-by-step reproduction
```

---

## Workflow 5: Report Writing

### Objective: Create professional vulnerability report

#### Report Structure:

```markdown
# [SEVERITY] Vulnerability Title

## Executive Summary
One paragraph describing:
- What the vulnerability is
- How severe it is
- What the impact is

## Technical Details
### Vulnerability Type
CWE-XXX / OWASP category

### Affected Endpoint(s)
- URL: https://...
- Parameter: ...
- Component: ...

### Root Cause
Explanation of why this vulnerability exists

## Proof of Concept

### Prerequisites
What is needed to reproduce

### Step-by-Step Reproduction
1. Step one
2. Step two
3. Step three

### Evidence
Screenshots, code snippets, request/response

## Impact Assessment
### What an Attacker Can Do
- Point 1
- Point 2

### Business Risk
Explanation of real-world consequences

## Remediation

### Immediate Fix
Specific code/configuration change

### Long-term Recommendations
- Defense in depth
- Security controls
- Code review areas

### References
- CWE entry
- OWASP guidance
- Similar CVEs
```

---

## Workflow 6: Submission & Follow-up

### Objective: Submit report and support remediation

```
STEP 1: Review Report
- Proofread for clarity
- Verify all links work
- Check attachments
- Ensure no sensitive data exposed

STEP 2: Submit
- Use program's submission platform
- Follow required format
- Attach all evidence
- Set appropriate severity

STEP 3: Respond to Questions
- Monitor for triager questions
- Provide additional details promptly
- Clarify reproduction steps if needed
- Stay professional

STEP 4: Verify Fix
- Test patch when deployed
- Confirm vulnerability resolved
- Check for bypass opportunities
- Report verification results

STEP 5: Disclosure (if applicable)
- Follow program disclosure policy
- Prepare public writeup (if allowed)
- Share knowledge responsibly
```

---

## Emergency Procedures

### If You Discover a Critical Vulnerability:

```
1. STOP testing immediately
2. Document what you found
3. Do not attempt further exploitation
4. Prepare preliminary report
5. Submit as quickly as possible
6. Mark as critical severity
```

### If You Accidentally Access Sensitive Data:

```
1. STOP immediately
2. Do not download or save data
3. Document what you accessed
4. Report in your submission
5. Delete any accidental copies
6. Request guidance from program
```

### If You Suspect You're Out of Scope:

```
1. STOP testing that asset
2. Review scope documentation
3. If unclear, ask program for clarification
4. Do not resume until confirmed
```

---

## Time Estimates

| Phase | Minimum | Recommended |
|-------|---------|-------------|
| Reconnaissance | 2 hours | 4-6 hours |
| Authentication Testing | 2 hours | 4 hours |
| IDOR Testing | 2 hours | 3 hours |
| Injection Testing | 3 hours | 5 hours |
| API Testing | 3 hours | 5 hours |
| Business Logic | 2 hours | 4 hours |
| Report Writing | 1 hour/bug | 2 hours/bug |

**Total for first bug:** 15-30 hours

---

*Open-Bounty Operating Instructions v2.0*
