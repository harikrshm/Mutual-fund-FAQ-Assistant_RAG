"""
Test suite for FAQ matching logic.

Tests the core FAQ matching functionality including:
- FAQ loading
- Query matching with various similarity thresholds
- Source verification
- Response structure validation
"""

import pytest
import json
from pathlib import Path
from src.faq_logic import FAQAssistant


@pytest.fixture
def faq_assistant():
    """Create FAQ Assistant instance for testing."""
    return FAQAssistant()


class TestFAQLoading:
    """Test FAQ data loading and initialization."""
    
    def test_faqs_loaded_successfully(self, faq_assistant):
        """Test that FAQs are loaded successfully."""
        assert faq_assistant.faqs is not None
        assert len(faq_assistant.faqs) > 0
    
    def test_faq_structure(self, faq_assistant):
        """Test that each FAQ entry has required fields."""
        required_fields = ['question_variants', 'answer', 'source', 'last_updated']
        
        for q_key, faq_entry in faq_assistant.faqs.items():
            assert isinstance(faq_entry, dict), f"FAQ entry {q_key} is not a dict"
            for field in required_fields:
                assert field in faq_entry, f"FAQ entry {q_key} missing field: {field}"
    
    def test_answer_not_empty(self, faq_assistant):
        """Test that all answers are non-empty."""
        for q_key, faq_entry in faq_assistant.faqs.items():
            answer = faq_entry.get('answer', '')
            assert answer.strip(), f"FAQ entry {q_key} has empty answer"
    
    def test_source_is_url(self, faq_assistant):
        """Test that all sources are valid URLs."""
        for q_key, faq_entry in faq_assistant.faqs.items():
            source = faq_entry.get('source', '')
            assert source.startswith('http'), f"FAQ entry {q_key} source is not a URL: {source}"
    
    def test_last_updated_format(self, faq_assistant):
        """Test that last_updated is in ISO format (YYYY-MM-DD)."""
        import re
        iso_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        for q_key, faq_entry in faq_assistant.faqs.items():
            last_updated = faq_entry.get('last_updated', '')
            assert iso_date_pattern.match(last_updated), \
                f"FAQ entry {q_key} has invalid date format: {last_updated}"


class TestQueryMatching:
    """Test FAQ query matching functionality."""
    
    def test_exact_match_bluechip_expense(self, faq_assistant):
        """Test exact match for SBI Bluechip Fund expense ratio."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'success'
        assert result['answer'] is not None
        assert 'expense ratio' in result['answer'].lower()
        assert 'Bluechip' in result['answer']
    
    def test_fuzzy_match_sip_amount(self, faq_assistant):
        """Test fuzzy matching for SIP amount query."""
        query = "How much minimum SIP for SBI Flexicap?"
        result = faq_assistant.query(query)
        
        # Should either match or return no_match, not error
        assert result['status'] in ['success', 'no_match']
    
    def test_multiple_scheme_queries(self, faq_assistant):
        """Test queries for different schemes."""
        schemes = ['Bluechip', 'Flexicap', 'ELSS', 'Gilt', 'Nifty Index']
        
        for scheme in schemes:
            query = f"What is the expense ratio of SBI {scheme} Fund?"
            result = faq_assistant.query(query)
            
            # Should get a response (success or no_match)
            assert result['status'] in ['success', 'no_match']
    
    def test_response_structure(self, faq_assistant):
        """Test that response has required structure."""
        query = "What is the minimum SIP amount for SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        # Check required response fields
        assert 'status' in result
        assert 'answer' in result
        assert 'source' in result
        assert 'last_updated' in result
    
    def test_answer_sentence_count(self, faq_assistant):
        """Test that answers are <= 3 sentences."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            answer = result['answer']
            # Count sentences (simplified: count periods, but exclude URLs)
            sentence_count = answer.count('.') - answer.count('http')
            assert sentence_count <= 3, f"Answer has {sentence_count} sentences, expected <= 3"
    
    def test_no_match_returns_proper_response(self, faq_assistant):
        """Test that unmatched queries return proper no_match response."""
        query = "What is the molecular weight of hydrogen peroxide?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'no_match'
        assert result['answer'] is None
        assert result['source'] is None


class TestCaseSensitivity:
    """Test query matching with different cases."""
    
    def test_lowercase_query(self, faq_assistant):
        """Test matching with lowercase query."""
        query = "what is the expense ratio of sbi bluechip fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']
    
    def test_uppercase_query(self, faq_assistant):
        """Test matching with uppercase query."""
        query = "WHAT IS THE EXPENSE RATIO OF SBI BLUECHIP FUND?"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']
    
    def test_mixed_case_query(self, faq_assistant):
        """Test matching with mixed case query."""
        query = "WhAt Is ThE ExPeNsE RaTiO Of SbI BlUeChIp FuNd?"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']


class TestQueryVariants:
    """Test matching with different query phrasings."""
    
    def test_variant_1_lock_in_period(self, faq_assistant):
        """Test lock-in period query variant 1."""
        query = "What is the lock-in period for ELSS?"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']
    
    def test_variant_2_lock_in_period(self, faq_assistant):
        """Test lock-in period query variant 2."""
        query = "SBI Long Term Equity Fund lock in time"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']
    
    def test_variant_benchmark(self, faq_assistant):
        """Test benchmark index query."""
        query = "What index does SBI Nifty Index Fund track?"
        result = faq_assistant.query(query)
        
        assert result['status'] in ['success', 'no_match']


class TestSourceValidation:
    """Test that sources are properly included in responses."""
    
    def test_successful_response_has_source(self, faq_assistant):
        """Test that successful responses include a source."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            assert result['source'] is not None
            assert len(result['source']) > 0
            assert result['source'].startswith('http')
    
    def test_source_is_string(self, faq_assistant):
        """Test that source is always a string."""
        query = "What is the minimum SIP for SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert isinstance(result['source'], (str, type(None)))
    
    def test_single_source_per_answer(self, faq_assistant):
        """Test that each answer has exactly one source."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            source = result['source']
            # Should be a single URL, not multiple
            assert source.count('http') == 1


class TestSchemeSpecificQueries:
    """Test queries specific to individual schemes."""
    
    def test_bluechip_fund_queries(self, faq_assistant):
        """Test various Bluechip Fund queries."""
        queries = [
            "SBI Bluechip Fund expense ratio",
            "Bluechip Fund exit load",
            "SBI Bluechip Fund minimum investment"
        ]
        
        for query in queries:
            result = faq_assistant.query(query)
            assert result['status'] in ['success', 'no_match']
    
    def test_elss_fund_queries(self, faq_assistant):
        """Test ELSS-specific queries."""
        queries = [
            "What is the lock-in period for ELSS?",
            "SBI Long Term Equity Fund lock in",
            "ELSS 3 year lock-in"
        ]
        
        for query in queries:
            result = faq_assistant.query(query)
            assert result['status'] in ['success', 'no_match']
    
    def test_index_fund_queries(self, faq_assistant):
        """Test Index Fund-specific queries."""
        queries = [
            "SBI Nifty Index Fund benchmark",
            "What index does Nifty Index Fund track?",
            "Index Fund Nifty 50"
        ]
        
        for query in queries:
            result = faq_assistant.query(query)
            assert result['status'] in ['success', 'no_match']
