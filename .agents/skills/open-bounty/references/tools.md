# Security Tools Reference

Essential tools for bug bounty hunting.

---

## Installation (Quick Setup)

```bash
# Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/ffuf/ffuf/v2@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/tomnomnom/anew@latest
go install github.com/tomnomnom/gf@latest

# Python tools
pip install sqlmap
pip install xsstrike

# Other
git clone https://github.com/OWASP/Amass.git
apt install gobuster nmap nikto
```

---

## Reconnaissance Tools

### Subdomain Enumeration

| Tool | Purpose | Command |
|------|---------|---------|
| amass | Comprehensive recon | `amass enum -passive -d target.com` |
| subfinder | Fast subdomain finder | `subfinder -d target.com -all` |
| assetfinder | Subdomain discovery | `assetfinder --subs-only target.com` |
| findomain | Cross-platform | `findomain -t target.com` |
| dnsgen | Permutation generation | `dnsgen domains.txt > permutations.txt` |

### HTTP Probing

| Tool | Purpose | Command |
|------|---------|---------|
| httpx | Fast HTTP prober | `httpx -l domains.txt` |
| httprobe | Alternative | `cat domains.txt | httprobe` |

### Port Scanning

| Tool | Purpose | Command |
|------|---------|---------|
| nmap | Comprehensive scanner | `nmap -sV -sC target.com` |
| naabu | Fast port scanner | `naabu -l domains.txt` |
| masscan | Internet-scale | `masscan -p1-65535 target.com` |

### URL Discovery

| Tool | Purpose | Command |
|------|---------|---------|
| waybackurls | Archive URLs | `waybackurls target.com` |
| gau | GetAllUrls | `gau target.com` |
| katana | Web crawler | `katana -u target.com` |
| hakrawler | Fast crawler | `echo target.com | hakrawler` |

---

## Vulnerability Scanners

### General Purpose

| Tool | Purpose | Command |
|------|---------|---------|
| nuclei | Template-based scanner | `nuclei -u target.com` |
| nuclei | Full scan | `nuclei -l urls.txt -severity critical,high` |
| nikto | Web vulnerability | `nikto -h target.com` |

### SQL Injection

| Tool | Purpose | Command |
|------|---------|---------|
| sqlmap | Automated SQLi | `sqlmap -u "URL?id=1" --batch` |
| sqlmap | Dump database | `sqlmap -u URL --dump` |
| sqlmap | OS shell | `sqlmap -u URL --os-shell` |

### XSS

| Tool | Purpose | Command |
|------|---------|---------|
| dalfox | Modern XSS scanner | `dalfox url target.com` |
| xsstrike | Advanced XSS | `python xsstrike.py -u target.com` |
| xsser | XSS framework | `xsser -u target.com` |

### Other Injection

| Tool | Purpose | Command |
|------|---------|---------|
| commix | Command injection | `python commix.py -u target.com` |
| tplmap | SSTI detection | `python tplmap.py -u target.com` |
| XXEinjector | XXE exploitation | `ruby XXEinjector.rb` |

---

## Fuzzing Tools

### Directory/Content

| Tool | Purpose | Command |
|------|---------|---------|
| ffuf | Fast fuzzer | `ffuf -u URL/FUZZ -w wordlist.txt` |
| gobuster | Directory brute | `gobuster dir -u URL -w wordlist.txt` |
| wfuzz | Web fuzzer | `wfuzz -w wordlist.txt URL/FUZZ` |
| dirsearch | Directory scan | `python dirsearch.py -u URL` |

### Parameter

| Tool | Purpose | Command |
|------|---------|---------|
| arjun | HTTP parameter | `arjun -u URL` |
| x8 | Hidden param finder | `x8 -u URL -w wordlist.txt` |
| param miner | Burp extension | (Burp Suite) |

### Wordlists

```
/usr/share/wordlists/
  - dirb/common.txt
  - dirbuster/directory-list-2.3-medium.txt
  - seclists/
    - Discovery/Web-Content/
    - Fuzzing/
    - Payloads/
```

---

## Proxy & Interception

| Tool | Platform | Best For |
|------|----------|----------|
| Burp Suite | Cross-platform | Professional testing |
| OWASP ZAP | Cross-platform | Open source option |
| Caido | Cross-platform | Modern alternative |
| mitmproxy | Cross-platform | Scripting/automation |
| Proxyman | macOS | macOS native |

---

## Specialized Tools

### JWT Testing

| Tool | Purpose | Command |
|------|---------|---------|
| jwt_tool | JWT analysis | `python jwt_tool.py TOKEN` |
| jwt-cracker | Crack JWT | `jwt-cracker TOKEN wordlist.txt` |

### CORS Testing

| Tool | Purpose |
|------|---------|
| CORStest | CORS misconfiguration |
| Corsy | Python CORS scanner |

### SSRF Testing

| Tool | Purpose | Command |
|------|---------|---------|
| SSRFmap | SSRF exploitation | `python ssrfmap.py -r request.txt` |
| Gopherus | SSRF payloads | `python Gopherus.py` |

### Subdomain Takeover

| Tool | Purpose | Command |
|------|---------|---------|
| subzy | Takeover checker | `subzy --targets domains.txt` |
| tko-subs | Takeover | `tko-subs -domains=domains.txt` |

### Secret Finding

| Tool | Purpose | Command |
|------|---------|---------|
| truffleHog | Git secrets | `trufflehog git URL` |
| gitLeaks | Git scanning | `gitleaks detect -v` |
| secretx | JS secrets | `cat urls.txt | secretx` |
| nuclei | Exposures | `nuclei -t exposures/` |

---

## Exploitation Tools

### Web Shells

| Tool | Purpose |
|------|---------|
| weevely | PHP web shell |
| b374k | PHP shell |
| China Chopper | Classic shell |

### Post-Exploitation

| Tool | Purpose |
|------|---------|
| netcat | Network Swiss army knife |
| socat | Advanced netcat |
| ngrok | Tunneling |

---

## Productivity Tools

### Data Processing

| Tool | Purpose | Example |
|------|---------|---------|
| jq | JSON processing | `cat file.json \| jq '.items[]'` |
| gron | JSON grep | `gron file.json \| grep value` |
| anew | Append new lines | `cat new.txt \| anew old.txt` |
| unfurl | URL analysis | `cat urls.txt \| unfurl -u domains` |

### Pattern Matching

| Tool | Purpose |
|------|---------|
| gf | grep on steroids |
| grep | Standard pattern |
| ripgrep | Fast grep |

---

## Browser Extensions

### For Manual Testing

| Extension | Purpose |
|-----------|---------|
| Wappalyzer | Tech detection |
| FoxyProxy | Proxy switching |
| Cookie Editor | Cookie manipulation |
| ModHeader | Header modification |
| HackBar | Request crafting |
| Retire.js | Vulnerable JS libs |

---

## Docker Images

```bash
# ProjectDiscovery suite
docker pull projectdiscovery/nuclei:latest
docker pull projectdiscovery/subfinder:latest
docker pull projectdiscovery/httpx:latest

# Kali tools
docker pull kalilinux/kali-rolling

# SQLMap
docker pull paoloo/sqlmap
```

---

## Quick One-Liners

```bash
# Subdomain enum → live hosts → nuclei scan
subfinder -d target.com | httpx | nuclei

# All URLs → filter params → XSS check
gau target.com | gf xss | dalfox pipe

# JS files → secrets
cat urls.txt | grep "\.js" | while read url; do curl -s "$url"; done | grep -i "api_key\|secret"

# Wayback → params → SQLi test
waybackurls target.com | grep "?" | uro | head -100 | while read url; do sqlmap -u "$url" --batch; done
```
