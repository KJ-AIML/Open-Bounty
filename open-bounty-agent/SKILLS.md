---
name: open-bounty-skills
description: |
  Comprehensive skill definitions for the Open-Bounty agent. This file 
  maps specific capabilities to actionable procedures, tools, and outputs.
  Any agent using this framework should reference these skill definitions
  when performing bug bounty operations.
version: 2.0.0
---

# Open-Bounty Skills Reference

## Skill Categories

1. [Reconnaissance Skills](#reconnaissance-skills)
2. [Vulnerability Discovery Skills](#vulnerability-discovery-skills)
3. [Exploitation Skills](#exploitation-skills)
4. [Reporting Skills](#reporting-skills)
5. [Tool Proficiency](#tool-proficiency)

---

## Reconnaissance Skills

### SKILL-001: Scope Analysis
**Purpose:** Validate and understand bug bounty program scope

**Inputs:**
- Program URL (e.g., hackerone.com/program-name)
- Raw scope list (domains, IPs, wildcards)

**Outputs:**
- Structured scope document
- In-scope asset list
- Out-of-scope exclusions
- Testing constraints (rate limits, forbidden techniques)

**Procedure:**
1. Read program policy thoroughly
2. Extract explicit scope definitions
3. Identify wildcard patterns
4. Note any special restrictions
5. Document previously disclosed reports (if available)
6. Flag high-value targets within scope

**Success Criteria:**
- Clear list of authorized targets
- Understanding of program rules
- Knowledge of reward structure

---

### SKILL-002: Subdomain Enumeration
**Purpose:** Discover all subdomains of target domains

**Inputs:**
- Root domain(s)
- Scope constraints

**Outputs:**
- List of live subdomains
- Technology fingerprints
- HTTP response codes
- Screenshot availability (optional)

**Tools:**
- subfinder (passive enumeration)
- amass (comprehensive recon)
- assetfinder (quick discovery)
- httpx (live host probing)

**Procedure:**
1. Run passive enumeration tools
2. Query certificate transparency logs
3. Check DNS records and permutations
4. Probe for live hosts
5. Filter out-of-scope results
6. Prioritize by technology/interest

---

### SKILL-003: Technology Detection
**Purpose:** Identify tech stack and potential vulnerability indicators

**Inputs:**
- URLs to analyze

**Outputs:**
- Web server software
- Programming frameworks
- JavaScript libraries
- CMS platforms
- Known CVE associations

**Tools:**
- Wappalyzer
- BuiltWith
- Nuclei (tech detection templates)
- Manual header analysis

**Procedure:**
1. Analyze HTTP headers
2. Check HTML meta tags and comments
3. Review JavaScript includes
4. Look for error messages
5. Check cookies for framework indicators
6. Correlate with known vulnerabilities

---

### SKILL-004: Content Discovery
**Purpose:** Find hidden endpoints, files, and directories

**Inputs:**
- Target URLs
- Wordlists

**Outputs:**
- Discovered endpoints
- API documentation locations
- Backup files
- Admin panels
- Configuration files

**Tools:**
- gobuster (directory brute force)
- ffuf (fast fuzzing)
- waybackurls (archive discovery)
- gau (URL enumeration)

**Procedure:**
1. Directory brute-forcing with common wordlists
2. Archive.org historical URL discovery
3. JavaScript endpoint extraction
4. API path enumeration
5. Backup file checking (.bak, .old, .zip)
6. Git exposure verification

---

## Vulnerability Discovery Skills

### SKILL-101: Authentication Testing
**Purpose:** Find weaknesses in login, registration, and password flows

**Test Vectors:**
- Password reset token predictability
- Username enumeration
- Brute force protection bypass
- Session management flaws
- JWT implementation issues
- OAuth misconfigurations
- MFA bypass techniques

**Tools:**
- Burp Suite / OWASP ZAP
- jwt_tool
- Custom Python scripts

**Outputs:**
- Authentication flow analysis
- Token entropy assessment
- Session handling evaluation
- Vulnerability evidence

---

### SKILL-102: IDOR Detection
**Purpose:** Find Insecure Direct Object Reference vulnerabilities

**Test Vectors:**
- Numeric ID manipulation (+1, -1, sequential)
- UUID pattern analysis
- Parameter pollution
- Batch endpoint abuse
- Cross-user data access

**Indicators:**
- URLs with numeric IDs (/users/123)
- API endpoints with object references
- Profile/account management pages
- Download/export functionality

**Outputs:**
- IDOR vulnerability confirmation
- Affected endpoint list
- Impact assessment
- Reproduction steps

---

### SKILL-103: Injection Testing
**Purpose:** Detect SQLi, XSS, Command Injection, and related flaws

**Test Categories:**

**SQL Injection:**
- Error-based detection
- Boolean-based blind
- Time-based blind
- Union-based extraction
- Stacked queries

**Cross-Site Scripting (XSS):**
- Reflected XSS in URL parameters
- Stored XSS in persistent storage
- DOM XSS in client-side JavaScript
- Blind XSS via out-of-band

**Command Injection:**
- OS command injection
- Template injection (SSTI)
- LDAP injection
- XPath injection

**Tools:**
- sqlmap (automated SQLi)
- dalfox (XSS detection)
- XSStrike
- Commix (command injection)

---

### SKILL-104: API Security Testing
**Purpose:** Test REST, GraphQL, and WebSocket APIs

**Test Vectors:**
- Authentication bypass
- Authorization failures (IDOR)
- Mass assignment
- Rate limiting bypass
- GraphQL introspection abuse
- Parameter tampering
- Versioning issues

**Tools:**
- Postman / Insomnia
- Burp Suite Repeater
- GraphQL introspection queries
- Custom API fuzzing scripts

---

### SKILL-105: Business Logic Testing
**Purpose:** Find flaws in application workflow and logic

**Common Issues:**
- Price/quantity manipulation
- Workflow bypass
- Race conditions
- Time-based attacks
- State machine abuse
- Feature abuse

**Methodology:**
1. Understand business flow
2. Identify trust boundaries
3. Test edge cases
4. Attempt negative scenarios
5. Race multiple requests
6. Skip intermediate steps

---

### SKILL-106: Cloud Security Assessment
**Purpose:** Find misconfigurations in cloud infrastructure

**Test Areas:**
- S3 bucket permissions
- IAM role misconfigurations
- Exposed storage buckets
- Cloud credentials in code
- Container registry exposure
- Kubernetes API access

**Tools:**
- cloud_enum
- s3scanner
- GrayHatWarfare
- truffleHog (secret scanning)

---

## Exploitation Skills

### SKILL-201: Proof-of-Concept Creation
**Purpose:** Validate vulnerabilities with minimal, safe exploits

**Principles:**
- Do no harm
- Minimal necessary demonstration
- Document exact conditions
- Reversible actions only

**Outputs:**
- Step-by-step reproduction guide
- Request/response samples
- Screenshots or video evidence
- Impact demonstration

---

### SKILL-202: Impact Assessment
**Purpose:** Determine real-world business impact of vulnerabilities

**Factors:**
- Data sensitivity (PII, credentials, financial)
- User scope (single user vs. all users)
- System access level (read vs. write vs. execute)
- Compliance implications
- Financial/reputational damage

**CVSS Scoring:**
- Calculate base score
- Consider temporal factors
- Account for environmental modifiers
- Map to program severity guidelines

---

## Reporting Skills

### SKILL-301: Technical Report Writing
**Purpose:** Create professional vulnerability reports

**Structure:**
1. Executive Summary
2. Technical Details
3. Proof of Concept
4. Impact Assessment
5. Remediation Recommendations

**Quality Standards:**
- Clear, concise language
- Specific technical details
- Reproducible steps
- Evidence attachments
- Professional tone

---

### SKILL-302: Remediation Guidance
**Purpose:** Provide actionable fix recommendations

**Components:**
- Root cause explanation
- Specific code/configuration fixes
- Defense in depth suggestions
- Verification steps
- Reference materials

---

## Tool Proficiency

### Category: Reconnaissance
| Tool | Proficiency | Use Case |
|------|-------------|----------|
| subfinder | Expert | Subdomain enumeration |
| amass | Expert | Comprehensive recon |
| httpx | Expert | Live host probing |
| gobuster | Expert | Directory brute force |
| ffuf | Expert | Fast fuzzing |
| nuclei | Advanced | Vulnerability scanning |

### Category: Exploitation
| Tool | Proficiency | Use Case |
|------|-------------|----------|
| sqlmap | Expert | SQL injection testing |
| dalfox | Advanced | XSS detection |
| burpsuite | Expert | Web proxy & testing |
| jwt_tool | Advanced | JWT analysis |

### Category: Analysis
| Tool | Proficiency | Use Case |
|------|-------------|----------|
| jq | Expert | JSON processing |
| grep/ripgrep | Expert | Pattern matching |
| curl/httpie | Expert | HTTP requests |

---

## Skill Activation Matrix

When user requests:

| User Request | Primary Skill | Secondary Skills |
|--------------|---------------|------------------|
| "Find subdomains" | SKILL-002 | SKILL-003 |
| "Test authentication" | SKILL-101 | SKILL-201 |
| "Look for IDOR" | SKILL-102 | SKILL-104 |
| "Check for SQLi" | SKILL-103 | SKILL-201 |
| "Test API" | SKILL-104 | SKILL-102 |
| "Find cloud misconfigs" | SKILL-106 | SKILL-002 |
| "Write report" | SKILL-301 | SKILL-302 |

---

*Open-Bounty Skills Framework v2.0*
