#!/usr/bin/env python3
"""
Open-Bounty Quick Wins Scanner
Checks for low-hanging fruit vulnerabilities

Usage: python quick_wins.py https://target.com
"""

import sys
import requests
import urllib3
from urllib.parse import urljoin, urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QuickWinsScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.findings = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        self.session.headers.update({
            'User-Agent': 'Open-Bounty-Scanner/2.0'
        })
    
    def check_git_exposure(self):
        """Check for exposed .git directories"""
        print("[*] Checking for .git exposure...")
        
        git_paths = [
            '/.git/',
            '/.git/config',
            '/.git/HEAD',
            '/.git/index'
        ]
        
        for path in git_paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url)
                if resp.status_code == 200:
                    content = resp.text
                    if '[core]' in content or 'ref:' in content or 'repositoryformatversion' in content:
                        self.findings.append({
                            'severity': 'CRITICAL',
                            'type': 'Source Code Disclosure',
                            'url': url,
                            'evidence': 'Exposed .git directory'
                        })
                        print(f"  [!] CRITICAL: Git exposure at {path}")
                        return True
            except:
                pass
        
        print("  [-] No .git exposure found")
        return False
    
    def check_env_files(self):
        """Check for exposed environment files"""
        print("[*] Checking for .env files...")
        
        env_paths = [
            '/.env',
            '/.env.local',
            '/.env.production',
            '/config/.env',
            '/api/.env',
            '/admin/.env'
        ]
        
        for path in env_paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url)
                if resp.status_code == 200:
                    content = resp.text
                    if any(x in content for x in ['DB_PASSWORD', 'API_KEY', 'SECRET', 'AWS_']):
                        self.findings.append({
                            'severity': 'CRITICAL',
                            'type': 'Credential Exposure',
                            'url': url,
                            'evidence': 'Exposed .env with credentials'
                        })
                        print(f"  [!] CRITICAL: Credentials at {path}")
                        return True
            except:
                pass
        
        print("  [-] No exposed .env files found")
        return False
    
    def check_common_admin_panels(self):
        """Check for common admin panels"""
        print("[*] Checking for admin panels...")
        
        admin_paths = [
            '/admin',
            '/administrator',
            '/admin/login',
            '/admin-panel',
            '/dashboard',
            '/panel',
            '/manage',
            '/console',
            '/wp-admin',
            '/phpmyadmin'
        ]
        
        found = []
        for path in admin_paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url, allow_redirects=True)
                if resp.status_code in [200, 401, 403]:
                    found.append((path, resp.status_code))
                    if resp.status_code == 200:
                        self.findings.append({
                            'severity': 'MEDIUM',
                            'type': 'Information Disclosure',
                            'url': url,
                            'evidence': f'Admin panel accessible (status {resp.status_code})'
                        })
            except:
                pass
        
        if found:
            print(f"  [+] Found {len(found)} potential admin panels:")
            for path, status in found:
                print(f"      {path} (Status: {status})")
        else:
            print("  [-] No admin panels found")
        
        return len(found) > 0
    
    def check_robots_txt(self):
        """Check robots.txt for interesting paths"""
        print("[*] Checking robots.txt...")
        
        url = urljoin(self.target, '/robots.txt')
        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                content = resp.text
                disallowed = [line for line in content.split('\n') if 'Disallow:' in line]
                
                if disallowed:
                    print(f"  [+] Found {len(disallowed)} disallowed paths:")
                    for line in disallowed[:10]:  # Show first 10
                        print(f"      {line.strip()}")
                    
                    interesting = ['/admin', '/api', '/config', '/backup', '/.git', '/internal']
                    found_interesting = [line for line in disallowed if any(x in line for x in interesting)]
                    
                    if found_interesting:
                        self.findings.append({
                            'severity': 'LOW',
                            'type': 'Information Disclosure',
                            'url': url,
                            'evidence': f'robots.txt reveals interesting paths'
                        })
                        return True
        except:
            pass
        
        print("  [-] No robots.txt or nothing interesting")
        return False
    
    def check_security_headers(self):
        """Check for missing security headers"""
        print("[*] Checking security headers...")
        
        try:
            resp = self.session.get(self.target)
            headers = resp.headers
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME sniffing protection',
                'X-XSS-Protection': 'XSS filter'
            }
            
            missing = []
            for header, description in security_headers.items():
                if header not in headers:
                    missing.append((header, description))
            
            if missing:
                print(f"  [!] Missing {len(missing)} security headers:")
                for header, desc in missing:
                    print(f"      - {header} ({desc})")
                
                self.findings.append({
                    'severity': 'LOW',
                    'type': 'Security Misconfiguration',
                    'url': self.target,
                    'evidence': f'Missing headers: {[h[0] for h in missing]}'
                })
                return True
            else:
                print("  [+] All recommended security headers present")
        except:
            print("  [-] Could not check headers")
        
        return False
    
    def check_cors_misconfig(self):
        """Check for CORS misconfiguration"""
        print("[*] Checking CORS configuration...")
        
        try:
            # Test with arbitrary origin
            resp = self.session.get(
                self.target,
                headers={'Origin': 'https://evil.com'}
            )
            
            acao = resp.headers.get('Access-Control-Allow-Origin')
            acac = resp.headers.get('Access-Control-Allow-Credentials')
            
            if acao == '*':
                print("  [!] CORS allows any origin (*)")
                self.findings.append({
                    'severity': 'LOW',
                    'type': 'CORS Misconfiguration',
                    'url': self.target,
                    'evidence': 'Access-Control-Allow-Origin: *'
                })
                return True
            
            if acao == 'https://evil.com':
                print("  [!] CORS reflects arbitrary origin!")
                severity = 'HIGH' if acac == 'true' else 'MEDIUM'
                self.findings.append({
                    'severity': severity,
                    'type': 'CORS Misconfiguration',
                    'url': self.target,
                    'evidence': f'Reflects origin, credentials: {acac}'
                })
                return True
            
            print("  [+] CORS properly configured")
        except:
            print("  [-] Could not check CORS")
        
        return False
    
    def scan(self):
        """Run all quick win checks"""
        print(f"\n{'='*60}")
        print(f"Open-Bounty Quick Wins Scanner")
        print(f"Target: {self.target}")
        print(f"{'='*60}\n")
        
        self.check_git_exposure()
        self.check_env_files()
        self.check_common_admin_panels()
        self.check_robots_txt()
        self.check_security_headers()
        self.check_cors_misconfig()
        
        # Summary
        print(f"\n{'='*60}")
        print("SCAN COMPLETE")
        print(f"{'='*60}")
        print(f"Total findings: {len(self.findings)}")
        
        if self.findings:
            print("\n[!] Findings by severity:")
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = len([f for f in self.findings if f['severity'] == severity])
                if count > 0:
                    print(f"    {severity}: {count}")
            
            print("\n[+] Detailed findings:")
            for i, finding in enumerate(self.findings, 1):
                print(f"\n  {i}. [{finding['severity']}] {finding['type']}")
                print(f"      URL: {finding['url']}")
                print(f"      Evidence: {finding['evidence']}")
        else:
            print("\n[+] No quick wins found. Proceed with deeper testing.")
        
        print(f"{'='*60}\n")
        
        return self.findings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_wins.py <target_url>")
        print("Example: python quick_wins.py https://example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = QuickWinsScanner(target)
    scanner.scan()
