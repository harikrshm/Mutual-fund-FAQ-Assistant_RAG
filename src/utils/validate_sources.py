"""
Validate sources.csv to ensure all URLs are from whitelisted official domains.

This script validates that all URLs in sources.csv are from trusted official domains:
- SBI Mutual Fund: sbmf.com, sbimf.com (and subdomains)
- AMFI: amfiindia.com (and subdomains)
- SEBI: sebi.gov.in (and subdomains)
"""

import csv
import sys
from urllib.parse import urlparse
from pathlib import Path


# Whitelist of official domains (base domains)
OFFICIAL_DOMAINS = [
    'sbmf.com',
    'sbimf.com',
    'amfiindia.com',
    'sebi.gov.in'
]


def extract_domain(url):
    """
    Extract the base domain from a URL.
    
    Args:
        url: Full URL string
        
    Returns:
        Base domain string (e.g., 'sbmf.com' from 'https://www.sbmf.com/path')
    """
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        
        # Remove port if present
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        
        # Remove 'www.' prefix if present
        if netloc.startswith('www.'):
            netloc = netloc[4:]
        
        return netloc
    except Exception as e:
        print(f"Error parsing URL {url}: {e}", file=sys.stderr)
        return None


def is_valid_domain(domain):
    """
    Check if a domain is in the whitelist or is a subdomain of a whitelisted domain.
    
    Args:
        domain: Domain string to validate
        
    Returns:
        True if domain is valid, False otherwise
    """
    if not domain:
        return False
    
    # Check exact match
    if domain in OFFICIAL_DOMAINS:
        return True
    
    # Check if it's a subdomain of any whitelisted domain
    for official_domain in OFFICIAL_DOMAINS:
        if domain.endswith('.' + official_domain):
            return True
    
    return False


def validate_sources_csv(csv_path):
    """
    Validate all URLs in sources.csv against the domain whitelist.
    
    Args:
        csv_path: Path to sources.csv file
        
    Returns:
        tuple: (is_valid, invalid_entries) where invalid_entries is a list of (row_num, url, domain)
    """
    invalid_entries = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                url = row.get('url', '').strip()
                domain = row.get('domain', '').strip()
                
                if not url:
                    continue
                
                # Extract domain from URL if not provided in CSV
                if not domain:
                    domain = extract_domain(url)
                
                # Validate domain
                if not is_valid_domain(domain):
                    invalid_entries.append((row_num, url, domain))
    
    except FileNotFoundError:
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        return False, []
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        return False, []
    
    return len(invalid_entries) == 0, invalid_entries


def main():
    """Main function to run domain validation."""
    # Get the project root directory (parent of src/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    csv_path = project_root / 'src' / 'data' / 'sources.csv'
    
    # Allow custom CSV path via command line argument
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    
    if not csv_path.exists():
        print(f"Error: sources.csv not found at {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Validating sources in: {csv_path}")
    print(f"Whitelisted domains: {', '.join(OFFICIAL_DOMAINS)}")
    print("-" * 60)
    
    is_valid, invalid_entries = validate_sources_csv(csv_path)
    
    if is_valid:
        print("[OK] All URLs are from whitelisted official domains.")
        sys.exit(0)
    else:
        print(f"[ERROR] Found {len(invalid_entries)} URL(s) from non-whitelisted domains:\n")
        for row_num, url, domain in invalid_entries:
            print(f"  Row {row_num}: {url}")
            print(f"    Domain: {domain}")
            print()
        sys.exit(1)


if __name__ == '__main__':
    main()

