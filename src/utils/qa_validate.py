"""
Validate faqs.json to ensure all entries have required fields and valid data.

This script validates that all FAQ entries have:
- question_variants (non-empty array)
- answer (non-empty string)
- source (valid URL format)
- last_updated (valid ISO date format YYYY-MM-DD)
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


# ISO date format regex (YYYY-MM-DD)
ISO_DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def validate_url(url):
    """
    Validate if a string is a valid URL format.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_iso_date(date_str):
    """
    Validate if a string is a valid ISO date format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid ISO date, False otherwise
    """
    if not ISO_DATE_PATTERN.match(date_str):
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_faq_entry(q_key, entry):
    """
    Validate a single FAQ entry.
    
    Args:
        q_key: Key of the FAQ entry
        entry: FAQ entry dictionary
        
    Returns:
        tuple: (is_valid, errors) where errors is a list of error messages
    """
    errors = []
    
    # Check question_variants
    if 'question_variants' not in entry:
        errors.append(f"Missing 'question_variants' field")
    elif not isinstance(entry['question_variants'], list):
        errors.append(f"'question_variants' must be a list")
    elif len(entry['question_variants']) == 0:
        errors.append(f"'question_variants' is empty")
    
    # Check answer
    if 'answer' not in entry:
        errors.append(f"Missing 'answer' field")
    elif not isinstance(entry['answer'], str):
        errors.append(f"'answer' must be a string")
    elif len(entry['answer'].strip()) == 0:
        errors.append(f"'answer' is empty")
    
    # Check source
    if 'source' not in entry:
        errors.append(f"Missing 'source' field")
    elif not isinstance(entry['source'], str):
        errors.append(f"'source' must be a string")
    elif not validate_url(entry['source']):
        errors.append(f"'source' is not a valid URL: {entry['source']}")
    
    # Check last_updated
    if 'last_updated' not in entry:
        errors.append(f"Missing 'last_updated' field")
    elif not isinstance(entry['last_updated'], str):
        errors.append(f"'last_updated' must be a string")
    elif not validate_iso_date(entry['last_updated']):
        errors.append(f"'last_updated' is not a valid ISO date (YYYY-MM-DD): {entry['last_updated']}")
    
    # Optional fields check (scheme_name, category)
    if 'scheme_name' not in entry:
        errors.append(f"Warning: Missing 'scheme_name' field (optional but recommended)")
    if 'category' not in entry:
        errors.append(f"Warning: Missing 'category' field (optional but recommended)")
    
    return len([e for e in errors if not e.startswith('Warning')]) == 0, errors


def validate_faqs_json(json_path):
    """
    Validate all FAQ entries in faqs.json.
    
    Args:
        json_path: Path to faqs.json file
        
    Returns:
        tuple: (is_valid, invalid_entries) where invalid_entries is a list of (q_key, errors)
    """
    invalid_entries = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_path}", file=sys.stderr)
        return False, []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
        return False, []
    except Exception as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        return False, []
    
    if not isinstance(faqs, dict):
        print("Error: faqs.json must be a JSON object/dictionary", file=sys.stderr)
        return False, []
    
    # Validate each entry
    for q_key, entry in faqs.items():
        is_valid, errors = validate_faq_entry(q_key, entry)
        if not is_valid or errors:  # Include warnings too
            invalid_entries.append((q_key, errors))
    
    return len([e for q, errs in invalid_entries if any(not err.startswith('Warning') for err in errs)]) == 0, invalid_entries


def main():
    """Main function to run FAQ validation."""
    # Get the project root directory (parent of src/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    json_path = project_root / 'src' / 'data' / 'faqs.json'
    
    # Allow custom JSON path via command line argument
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    
    if not json_path.exists():
        print(f"Error: faqs.json not found at {json_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Validating FAQs in: {json_path}")
    print("-" * 60)
    
    is_valid, invalid_entries = validate_faqs_json(json_path)
    
    if is_valid and len([e for _, errs in invalid_entries for err in errs if not err.startswith('Warning')]) == 0:
        warnings = [e for _, errs in invalid_entries for err in errs if err.startswith('Warning')]
        if warnings:
            print("[WARNING] Found warnings (non-critical):")
            for q_key, errors in invalid_entries:
                for error in errors:
                    if error.startswith('Warning'):
                        print(f"  {q_key}: {error}")
            print()
        print("[OK] All FAQ entries are valid.")
        sys.exit(0)
    else:
        print(f"[ERROR] Found {len([e for _, errs in invalid_entries for err in errs if not err.startswith('Warning')])} validation error(s):\n")
        for q_key, errors in invalid_entries:
            critical_errors = [e for e in errors if not e.startswith('Warning')]
            if critical_errors:
                print(f"  {q_key}:")
                for error in critical_errors:
                    print(f"    - {error}")
                print()
        sys.exit(1)


if __name__ == '__main__':
    main()

