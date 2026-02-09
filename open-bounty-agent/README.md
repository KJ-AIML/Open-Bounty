# Open-Bounty Agent Framework v2.0

> A universal, model-agnostic framework for AI agents performing authorized bug bounty hunting and security assessments.

---

## 🎯 What is Open-Bounty?

Open-Bounty is a comprehensive framework that transforms any AI agent into an elite bug bounty hunter. It provides:

- **Structured Methodologies** - Step-by-step testing procedures
- **Professional Templates** - Report formats that get paid
- **Reusable Tools** - Scripts for common tasks
- **Clear Instructions** - How to think, act, and report like a security researcher

### Core Philosophy

> **Ethics first, precision over speed, protect users, get paid.**

---

## 📁 Framework Structure

```
open-bounty-agent/
├── AGENTS.md                 # Who you are (identity & principles)
├── SKILLS.md                 # What you can do (capabilities)
├── INSTRUCTIONS.md           # How to operate (workflows)
├── README.md                 # This file
│
├── methodology/              # Testing guides
│   ├── authentication-testing.md
│   ├── idor-testing.md
│   └── api-security-testing.md
│
├── templates/                # Report templates
│   ├── vulnerability-report.md
│   └── recon-report.md
│
├── tools/                    # Reusable scripts
│   ├── subdomain_enum.sh
│   └── quick_wins.py
│
└── examples/                 # Example reports & findings
    └── (populate with your work)
```

---

## 🚀 Quick Start

### For AI Agents

When a user asks you to help with bug bounty hunting:

1. **Read AGENTS.md** - Understand your identity as Open-Bounty
2. **Read INSTRUCTIONS.md** - Know the workflows
3. **Reference SKILLS.md** - Match capabilities to requests
4. **Follow Methodology** - Use appropriate testing guides
5. **Generate Reports** - Use templates for professional output

### For Human Users

```bash
# Clone or copy this framework
git clone <repository> open-bounty-agent
cd open-bounty-agent

# Start with reconnaissance
./tools/subdomain_enum.sh target.com

# Run quick wins scan
python tools/quick_wins.py https://target.com

# Follow methodology guides for deep testing
# Use templates for reporting
```

---

## 📖 Documentation Guide

### AGENTS.md - Your Identity
**When to read:** At the start of every engagement

**Key sections:**
- Who You Are - Your mission and principles
- What You Do - Core capabilities
- How You Think - Attacker mindset with ethics
- Knowledge Domains - Areas of expertise

### SKILLS.md - Your Capabilities
**When to read:** When planning specific tests

**Key sections:**
- Reconnaissance Skills - How to map targets
- Vulnerability Discovery - Testing techniques
- Exploitation Skills - Safe proof-of-concepts
- Reporting Skills - Documentation

### INSTRUCTIONS.md - Your Workflows
**When to read:** During operations for step-by-step guidance

**Key sections:**
- Workflow 1: Initial Engagement
- Workflow 2: Reconnaissance
- Workflow 3: Vulnerability Discovery
- Workflow 4: Validation
- Workflow 5: Report Writing
- Workflow 6: Submission

---

## 🔍 Testing Methodologies

### Authentication Testing
**File:** `methodology/authentication-testing.md`

Covers:
- Username enumeration
- Password reset token analysis
- Brute force protection
- Session management
- JWT security
- MFA bypass

### IDOR Testing
**File:** `methodology/idor-testing.md`

Covers:
- Numeric ID manipulation
- GUID/UUID testing
- Parameter pollution
- Mass assignment
- Advanced techniques

### API Security Testing
**File:** `methodology/api-security-testing.md`

Covers:
- REST API testing
- GraphQL security
- Authentication bypass
- Authorization testing
- Input validation

---

## 📝 Report Templates

### Vulnerability Report
**File:** `templates/vulnerability-report.md`

Use for:
- HackerOne submissions
- Bugcrowd reports
- Direct disclosure
- Internal security teams

**Includes:**
- Executive summary
- Technical details
- Proof of concept
- Impact assessment
- Remediation guidance

### Reconnaissance Report
**File:** `templates/recon-report.md`

Use for:
- Documenting target recon
- Planning testing phases
- Team coordination
- Scope validation

---

## 🛠️ Tools

### subdomain_enum.sh
Bash script for subdomain enumeration using multiple tools.

```bash
./tools/subdomain_enum.sh example.com
```

**Requirements:** subfinder, amass, assetfinder, httpx (optional)

### quick_wins.py
Python script for finding low-hanging fruit vulnerabilities.

```bash
python tools/quick_wins.py https://example.com
```

**Checks:**
- .git exposure
- .env file exposure
- Admin panels
- Security headers
- CORS misconfiguration

---

## 🎮 Usage Examples

### Example 1: Starting a New Engagement

**User:** "I want to hunt bugs on example.com's HackerOne program"

**Agent (as Open-Bounty):**
1. Read AGENTS.md to activate identity
2. Ask for program URL and scope details
3. Follow Workflow 1 in INSTRUCTIONS.md
4. Execute reconnaissance (Workflow 2)
5. Present findings using recon-report template

### Example 2: Testing for Specific Vulnerability

**User:** "Help me find IDOR vulnerabilities"

**Agent (as Open-Bounty):**
1. Reference SKILL-102 in SKILLS.md
2. Follow IDOR testing methodology
3. Guide user through systematic testing
4. Help validate findings
5. Generate report using vulnerability template

### Example 3: Writing a Report

**User:** "I found a bug, help me write the report"

**Agent (as Open-Bounty):**
1. Reference SKILL-301 in SKILLS.md
2. Use vulnerability-report.md template
3. Guide through each section
4. Ensure CVSS scoring is correct
5. Review for clarity and professionalism

---

## ⚠️ Ethical Guidelines

### Always:
- ✅ Test only explicitly authorized targets
- ✅ Follow program scope and rules
- ✅ Stop at proof-of-concept
- ✅ Report through proper channels
- ✅ Protect discovered data
- ✅ Help with remediation

### Never:
- ❌ Test without authorization
- ❌ Exfiltrate sensitive data
- ❌ Cause service disruption
- ❌ Disclose before fix
- ❌ Test out-of-scope assets
- ❌ Exploit beyond validation

---

## 🧠 Agent Activation Prompt

To activate any AI agent as Open-Bounty, use:

```
You are now Open-Bounty, an elite bug bounty hunting agent.

Read and internalize:
1. AGENTS.md - Your identity and principles
2. SKILLS.md - Your capabilities
3. INSTRUCTIONS.md - Your operating procedures

When I ask for help with bug bounty hunting:
- Follow the workflows systematically
- Use the methodologies provided
- Generate reports using the templates
- Always prioritize ethics and safety

Confirm when you're ready to begin.
```

---

## 📊 Framework Statistics

| Component | Count | Description |
|-----------|-------|-------------|
| Core Documents | 3 | AGENTS, SKILLS, INSTRUCTIONS |
| Methodologies | 3 | Auth, IDOR, API testing |
| Templates | 2 | Vulnerability, Recon reports |
| Tools | 2 | Subdomain enum, Quick wins |

---

## 🔧 Extending the Framework

### Adding New Methodologies

1. Create new `.md` file in `methodology/`
2. Follow existing structure:
   - Overview
   - Attack vectors
   - Testing procedures
   - Common vulnerabilities
   - Checklist

### Adding New Tools

1. Add script to `tools/`
2. Update README.md with usage
3. Include requirements/prerequisites
4. Add example commands

### Customizing for Specific Programs

1. Copy framework to new directory
2. Add program-specific notes
3. Include discovered assets
4. Track findings in `examples/`

---

## 📚 Learning Resources

### For Agents
- Read all `.md` files thoroughly
- Study methodology examples
- Understand report structure
- Learn CVSS scoring

### For Humans
- OWASP Testing Guide
- Bug Bounty Hunter's Methodology
- Web Application Hacker's Handbook
- PortSwigger Web Security Academy

---

## 🤝 Contributing

This framework is designed to be:
- **Universal** - Works with any AI agent
- **Extensible** - Easy to add new content
- **Practical** - Based on real bug bounty experience
- **Ethical** - Emphasizes responsible disclosure

To contribute:
1. Add new methodologies for other vulnerability types
2. Create additional tools and scripts
3. Improve templates based on successful reports
4. Share examples (sanitized)

---

## 📜 Version History

### v2.0.0 (Current)
- Universal agent framework
- Model-agnostic design
- Comprehensive methodologies
- Professional templates
- Reusable tools

### v1.0.0
- Initial 8x8-specific implementation
- Basic reconnaissance scripts
- Initial skill development

---

## 🏆 Success Metrics

Using this framework, agents should aim for:

| Level | Metric |
|-------|--------|
| Beginner | Submit first valid report |
| Intermediate | Find high/critical severity bug |
| Advanced | Earn $1,000+ in bounties |
| Expert | Consistent valid findings |

---

## 📞 Support

**For Agents:**
- Reference the framework documents
- Follow the decision trees in INSTRUCTIONS.md
- Use methodology checklists

**For Users:**
- Start with quick wins scan
- Follow methodologies step-by-step
- Use report templates as guides

---

## 🛡️ Legal Notice

This framework is for **authorized security testing only**.

- Only use on systems you have explicit permission to test
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Respect program terms of service

**The authors assume no liability for misuse of this framework.**

---

## 🌟 Acknowledgments

This framework draws from:
- OWASP Testing Methodology
- Bug Bounty community best practices
- Professional penetration testing standards
- Responsible disclosure guidelines

---

**Open-Bounty Framework v2.0**  
**For authorized security testing only**  
**Protect users. Find bugs. Get paid.** 🐛💰
