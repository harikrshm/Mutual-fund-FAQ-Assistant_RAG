"""
FAQ Assistant Logic - Rule-based FAQ matching system.

This module provides functionality to:
- Load FAQs from JSON
- Match user queries against FAQ database using fuzzy matching
- Detect PII in queries
- Detect advice/refusal triggers
- Return formatted responses
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches, SequenceMatcher


# PII patterns
PAN_PATTERN = re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]')
AADHAAR_PATTERN = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
ACCOUNT_PATTERN = re.compile(r'\b\d{9,18}\b')

# Advice/refusal trigger words
ADVICE_TRIGGERS = [
    'buy', 'sell', 'should i', 'recommend', 'recommendation', 'advice',
    'suggest', 'suggestion', 'portfolio', 'invest in', 'worth investing',
    'good investment', 'bad investment', 'should invest', 'must invest'
]


class FAQAssistant:
    """FAQ Assistant that matches user queries against FAQ database."""
    
    def __init__(self, faqs_path: Optional[Path] = None):
        """
        Initialize FAQ Assistant.
        
        Args:
            faqs_path: Path to faqs.json file. If None, uses default path.
        """
        if faqs_path is None:
            # Default path: project_root/src/data/faqs.json
            script_dir = Path(__file__).parent
            faqs_path = script_dir / 'data' / 'faqs.json'
        
        self.faqs_path = faqs_path
        self.faqs = self._load_faqs()
    
    def _load_faqs(self) -> Dict:
        """Load FAQs from JSON file."""
        try:
            with open(self.faqs_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: FAQ file not found at {self.faqs_path}", file=sys.stderr)
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in FAQ file: {e}", file=sys.stderr)
            return {}
    
    def detect_pii(self, query: str) -> Tuple[bool, List[str]]:
        """
        Detect PII in user query.
        
        Args:
            query: User query string
            
        Returns:
            tuple: (has_pii, detected_patterns)
        """
        detected = []
        
        # Check for PAN
        if PAN_PATTERN.search(query):
            detected.append('PAN')
        
        # Check for Aadhaar
        if AADHAAR_PATTERN.search(query):
            detected.append('Aadhaar')
        
        # Check for account numbers (9-18 digits)
        if ACCOUNT_PATTERN.search(query):
            detected.append('Account Number')
        
        return len(detected) > 0, detected
    
    def detect_advice_request(self, query: str) -> bool:
        """
        Detect if query is requesting investment advice.
        
        Args:
            query: User query string
            
        Returns:
            True if advice is requested, False otherwise
        """
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in ADVICE_TRIGGERS)
    
    def fuzzy_match(self, query: str, threshold: float = 0.4) -> Optional[Tuple[str, Dict, float]]:
        """
        Find best matching FAQ using fuzzy matching.
        
        Args:
            query: User query string
            threshold: Minimum similarity threshold (0-1)
            
        Returns:
            tuple: (q_key, faq_entry, similarity_score) or None if no match
        """
        query_lower = query.lower().strip()
        best_match = None
        best_score = 0.0
        
        # Extract key terms from query
        query_terms = set(query_lower.split())
        
        # Collect all question variants and calculate similarity
        for q_key, faq_entry in self.faqs.items():
            question_variants = faq_entry.get('question_variants', [])
            for variant in question_variants:
                variant_lower = variant.lower()
                
                # Calculate multiple similarity metrics
                # 1. Sequence similarity
                sequence_sim = SequenceMatcher(None, query_lower, variant_lower).ratio()
                
                # 2. Word overlap similarity
                variant_terms = set(variant_lower.split())
                if query_terms and variant_terms:
                    overlap = len(query_terms & variant_terms) / len(query_terms | variant_terms)
                else:
                    overlap = 0.0
                
                # 3. Combined score (weighted average)
                combined_score = (sequence_sim * 0.6) + (overlap * 0.4)
                
                # 4. Check for substring match (boost score)
                if query_lower in variant_lower or variant_lower in query_lower:
                    combined_score = max(combined_score, 0.7)
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_match = (q_key, faq_entry, combined_score)
        
        return best_match if best_score >= threshold else None
    
    def query(self, user_query: str) -> Dict:
        """
        Process user query and return response.
        
        Args:
            user_query: User's question
            
        Returns:
            dict: Response with answer, source, last_updated, and status
        """
        # Check for PII
        has_pii, pii_types = self.detect_pii(user_query)
        if has_pii:
            return {
                'status': 'error',
                'error_type': 'pii_detected',
                'message': f'Personal information detected: {", ".join(pii_types)}. Please remove personal information from your query.',
                'answer': None,
                'source': None,
                'last_updated': None
            }
        
        # Check for advice request
        if self.detect_advice_request(user_query):
            return {
                'status': 'refusal',
                'error_type': 'advice_request',
                'message': 'This assistant provides factual information only and does not offer investment advice, recommendations, or portfolio suggestions. For investment guidance, please consult a registered financial advisor or visit AMFI at https://www.amfiindia.com/',
                'answer': None,
                'source': 'https://www.amfiindia.com/',
                'last_updated': None
            }
        
        # Try to match query
        match = self.fuzzy_match(user_query, threshold=0.5)
        
        if match:
            q_key, faq_entry, similarity = match
            return {
                'status': 'success',
                'answer': faq_entry.get('answer', ''),
                'source': faq_entry.get('source', ''),
                'last_updated': faq_entry.get('last_updated', ''),
                'matched_q_key': q_key,
                'similarity': similarity
            }
        else:
            return {
                'status': 'no_match',
                'error_type': 'no_match',
                'message': 'No matching FAQ found. Please try rephrasing your question or check the example questions below.',
                'answer': None,
                'source': None,
                'last_updated': None
            }


def main():
    """Main function for testing."""
    assistant = FAQAssistant()
    
    # Test queries
    test_queries = [
        "What is the expense ratio of SBI Bluechip Fund?",
        "What is the lock-in period for ELSS?",
        "Should I invest in mutual funds?",
        "My PAN is ABCDE1234F",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = assistant.query(query)
        print(f"Result: {json.dumps(result, indent=2)}")


if __name__ == '__main__':
    main()

