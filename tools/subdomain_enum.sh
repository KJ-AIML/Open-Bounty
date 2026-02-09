#!/bin/bash
# Open-Bounty Subdomain Enumeration Script
# Usage: ./subdomain_enum.sh domain.com

set -e

DOMAIN=$1
OUTPUT_DIR="recon_$DOMAIN_$(date +%Y%m%d)"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain>"
    echo "Example: $0 example.com"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Open-Bounty Subdomain Enumeration                     ║"
echo "║  Target: $DOMAIN                                       "
echo "╚════════════════════════════════════════════════════════╝"

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "[+] Output directory: $OUTPUT_DIR"

# Step 1: Passive Enumeration
echo ""
echo "[+] Step 1: Passive Subdomain Enumeration"
echo "─────────────────────────────────────────"

# subfinder
if command -v subfinder &> /dev/null; then
    echo "[*] Running subfinder..."
    subfinder -d "$DOMAIN" -all -o "$OUTPUT_DIR/subfinder.txt" 2>/dev/null || true
    echo "[+] subfinder complete"
else
    echo "[-] subfinder not found, skipping"
fi

# amass (passive)
if command -v amass &> /dev/null; then
    echo "[*] Running amass (passive)..."
    amass enum -passive -d "$DOMAIN" -o "$OUTPUT_DIR/amass.txt" 2>/dev/null || true
    echo "[+] amass complete"
else
    echo "[-] amass not found, skipping"
fi

# assetfinder
if command -v assetfinder &> /dev/null; then
    echo "[*] Running assetfinder..."
    assetfinder --subs-only "$DOMAIN" > "$OUTPUT_DIR/assetfinder.txt" 2>/dev/null || true
    echo "[+] assetfinder complete"
else
    echo "[-] assetfinder not found, skipping"
fi

# crt.sh
if command -v curl &> /dev/null; then
    echo "[*] Querying crt.sh..."
    curl -s "https://crt.sh/?q=%.$DOMAIN&output=json" | \
        jq -r '.[].name_value' 2>/dev/null | \
        sort -u > "$OUTPUT_DIR/crtsh.txt" || true
    echo "[+] crt.sh complete"
else
    echo "[-] curl not found, skipping crt.sh"
fi

# Step 2: Combine Results
echo ""
echo "[+] Step 2: Combining Results"
echo "─────────────────────────────"
cat "$OUTPUT_DIR"/*.txt 2>/dev/null | \
    grep -v "^$" | \
    sort -u > "$OUTPUT_DIR/all_subdomains.txt"

SUBDOMAIN_COUNT=$(wc -l < "$OUTPUT_DIR/all_subdomains.txt" 2>/dev/null || echo "0")
echo "[+] Total unique subdomains: $SUBDOMAIN_COUNT"

# Step 3: Probe for Live Hosts
echo ""
echo "[+] Step 3: Probing for Live Hosts"
echo "──────────────────────────────────"

if command -v httpx &> /dev/null; then
    echo "[*] Running httpx..."
    httpx -l "$OUTPUT_DIR/all_subdomains.txt" \
          -o "$OUTPUT_DIR/live_hosts.txt" \
          -status-code \
          -title \
          -tech-detect 2>/dev/null || true
    
    LIVE_COUNT=$(wc -l < "$OUTPUT_DIR/live_hosts.txt" 2>/dev/null || echo "0")
    echo "[+] Live hosts found: $LIVE_COUNT"
else
    echo "[-] httpx not found, skipping live host detection"
    echo "[!] Install httpx: go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
fi

# Step 4: Summary
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  Enumeration Complete                                  ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║  Results saved in: $OUTPUT_DIR"
echo "║  - all_subdomains.txt: $SUBDOMAIN_COUNT subdomains"
echo "║  - live_hosts.txt: $LIVE_COUNT live hosts"
echo "╚════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Next steps:"
echo "    1. Review $OUTPUT_DIR/all_subdomains.txt"
echo "    2. Check $OUTPUT_DIR/live_hosts.txt for interesting targets"
echo "    3. Run technology detection: ./tech_detect.sh $DOMAIN"
