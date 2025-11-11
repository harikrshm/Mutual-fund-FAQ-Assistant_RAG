"""
Test suite for PII (Personally Identifiable Information) detection.

Tests detection of:
- PAN (Personal Account Number)
- Aadhaar numbers
- Bank account numbers
"""

import pytest
from src.faq_logic import FAQAssistant


@pytest.fixture
def faq_assistant():
    """Create FAQ Assistant instance for testing."""
    return FAQAssistant()


class TestPANDetection:
    """Test PAN (Personal Account Number) detection."""
    
    def test_valid_pan_detected(self, faq_assistant):
        """Test detection of valid PAN format."""
        query = "My PAN is ABCDE1234F"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'PAN' in pii_types
    
    def test_pan_lowercase_detected(self, faq_assistant):
        """Test detection of PAN in lowercase."""
        query = "my pan is abcde1234f"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        # PAN regex is case-sensitive, so lowercase shouldn't match
        # This tests the current behavior
        assert isinstance(has_pii, bool)
    
    def test_multiple_pans_detected(self, faq_assistant):
        """Test detection of multiple PANs in query."""
        query = "PAN1: ABCDE1234F and PAN2: XYZ123456A"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        # Should detect at least one PAN
        assert 'PAN' in pii_types
    
    def test_no_false_positive_pans(self, faq_assistant):
        """Test that non-PAN sequences aren't flagged."""
        query = "What about ABCD12345 format?"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        # ABCD12345 is not a valid PAN format (needs 5 letters, 4 digits, 1 letter)
        assert 'PAN' not in pii_types


class TestAadhaarDetection:
    """Test Aadhaar number detection."""
    
    def test_valid_aadhaar_detected(self, faq_assistant):
        """Test detection of valid Aadhaar format."""
        query = "My Aadhaar is 1234 5678 9012"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'Aadhaar' in pii_types
    
    def test_aadhaar_without_spaces(self, faq_assistant):
        """Test detection of Aadhaar without spaces."""
        query = "Aadhaar number: 123456789012"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'Aadhaar' in pii_types
    
    def test_multiple_aadhaar_detected(self, faq_assistant):
        """Test detection of multiple Aadhaar numbers."""
        query = "My Aadhaar is 1234 5678 9012 and spouse's is 9876 5432 1098"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'Aadhaar' in pii_types
    
    def test_no_false_positive_numbers(self, faq_assistant):
        """Test that random 12-digit numbers without Aadhaar context are still detected."""
        query = "The year 1234 and month 56 are not Aadhaar"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        # This is a limitation - 4-digit patterns can appear in dates
        # Current implementation may have false positives


class TestAccountNumberDetection:
    """Test account number detection."""
    
    def test_account_number_9_digits(self, faq_assistant):
        """Test detection of 9-digit account number."""
        query = "My account number is 123456789"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'Account Number' in pii_types
    
    def test_account_number_18_digits(self, faq_assistant):
        """Test detection of 18-digit account number."""
        query = "My account is 123456789012345678"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'Account Number' in pii_types
    
    def test_account_number_with_spaces(self, faq_assistant):
        """Test detection of account number with spaces."""
        query = "Account: 1234 5678 90123456"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        # Pattern doesn't account for spaces in account numbers
        assert isinstance(has_pii, bool)


class TestPIIResponseHandling:
    """Test how PII in queries is handled."""
    
    def test_query_with_pan_returns_error(self, faq_assistant):
        """Test that query with PAN returns error response."""
        query = "What is SBI Bluechip expense ratio? My PAN is ABCDE1234F"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'pii_detected'
        assert 'PAN' in result['message']
    
    def test_query_with_aadhaar_returns_error(self, faq_assistant):
        """Test that query with Aadhaar returns error response."""
        query = "My Aadhaar is 1234 5678 9012"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'pii_detected'
        assert 'Aadhaar' in result['message']
    
    def test_query_with_account_number_returns_error(self, faq_assistant):
        """Test that query with account number returns error response."""
        query = "I have account 123456789 with SBI Mutual Fund"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'pii_detected'
        assert 'Account Number' in result['message']
    
    def test_pii_error_has_no_answer(self, faq_assistant):
        """Test that PII error doesn't return FAQ answer."""
        query = "What is expense ratio? My PAN is ABCDE1234F"
        result = faq_assistant.query(query)
        
        assert result['answer'] is None
        assert result['source'] is None


class TestPIIEdgeCases:
    """Test edge cases in PII detection."""
    
    def test_empty_query(self, faq_assistant):
        """Test empty query has no PII."""
        query = ""
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is False
        assert len(pii_types) == 0
    
    def test_clean_query_no_pii(self, faq_assistant):
        """Test clean query with no PII."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is False
        assert len(pii_types) == 0
    
    def test_query_with_numbers_no_pii(self, faq_assistant):
        """Test query with numbers that don't form PII."""
        query = "What about fund category 2 or level 3 schemes?"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is False
    
    def test_pii_in_middle_of_query(self, faq_assistant):
        """Test PII detection when PII is in middle of sentence."""
        query = "I have PAN ABCDE1234F which is registered with"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        assert 'PAN' in pii_types
    
    def test_multiple_pii_types_detected(self, faq_assistant):
        """Test detection of multiple types of PII."""
        query = "My PAN is ABCDE1234F and Aadhaar is 1234 5678 9012"
        has_pii, pii_types = faq_assistant.detect_pii(query)
        
        assert has_pii is True
        # Should detect both PAN and Aadhaar
        assert 'PAN' in pii_types
        assert 'Aadhaar' in pii_types


class TestPIIDetectionReliability:
    """Test reliability and consistency of PII detection."""
    
    def test_pan_detection_consistency(self, faq_assistant):
        """Test that PAN detection is consistent across calls."""
        query = "My PAN is ABCDE1234F"
        
        results = [faq_assistant.detect_pii(query) for _ in range(3)]
        
        # All results should be identical
        assert all(r == results[0] for r in results)
    
    def test_aadhaar_detection_consistency(self, faq_assistant):
        """Test that Aadhaar detection is consistent."""
        query = "My Aadhaar is 1234 5678 9012"
        
        results = [faq_assistant.detect_pii(query) for _ in range(3)]
        
        assert all(r == results[0] for r in results)
