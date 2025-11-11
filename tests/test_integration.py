"""
Integration tests for FAQ Assistant.

Tests the complete workflow including:
- FAQ query to response pipeline
- Compliance checks
- Source validity
- Answer format validation
"""

import pytest
from src.faq_logic import FAQAssistant


@pytest.fixture
def faq_assistant():
    """Create FAQ Assistant instance for testing."""
    return FAQAssistant()


class TestCompleteQueryFlow:
    """Test complete query to response flow."""
    
    def test_successful_query_flow(self, faq_assistant):
        """Test complete successful query flow."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'success'
        assert result['answer'] is not None
        assert result['source'] is not None
        assert result['last_updated'] is not None
    
    def test_pii_blocked_query_flow(self, faq_assistant):
        """Test query with PII is properly blocked."""
        query = "What is the expense? My PAN is ABCDE1234F"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'error'
        assert 'PII' in result['message'] or 'pii' in result['message'].lower()
        assert result['answer'] is None
    
    def test_advice_refused_query_flow(self, faq_assistant):
        """Test that advice request is refused."""
        query = "Should I invest in SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'refusal'
        assert result['answer'] is None
    
    def test_no_match_query_flow(self, faq_assistant):
        """Test query with no match."""
        query = "What is the square root of 16?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'no_match'
        assert result['answer'] is None


class TestAnswerFormatCompliance:
    """Test that answers meet format requirements."""
    
    def test_answer_not_too_long(self, faq_assistant):
        """Test that answers are not excessively long."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            answer = result['answer']
            # Rough check: answer should be reasonable length (not > 500 chars for fact)
            assert len(answer) < 500, "Answer seems too long"
    
    def test_answer_is_string(self, faq_assistant):
        """Test that answer is a string."""
        query = "What is the minimum SIP?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            assert isinstance(result['answer'], str)
    
    def test_answer_not_empty_on_success(self, faq_assistant):
        """Test that successful answers are not empty."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            assert len(result['answer'].strip()) > 0


class TestSourceCompliance:
    """Test that sources meet compliance requirements."""
    
    def test_source_is_url_on_success(self, faq_assistant):
        """Test that source is a valid URL on success."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            source = result['source']
            assert source.startswith('http://') or source.startswith('https://')
    
    def test_single_source_not_multiple(self, faq_assistant):
        """Test that only one source is returned."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            source = result['source']
            # Count occurrences of 'http'
            http_count = source.count('http')
            assert http_count == 1, "Multiple URLs in single source"


class TestLastUpdatedCompliance:
    """Test that last_updated field meets requirements."""
    
    def test_last_updated_present_on_success(self, faq_assistant):
        """Test that last_updated is present on success."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            assert result['last_updated'] is not None
            assert len(result['last_updated']) > 0
    
    def test_last_updated_format(self, faq_assistant):
        """Test that last_updated is in ISO format."""
        import re
        iso_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            date_str = result['last_updated']
            assert iso_pattern.match(date_str), \
                f"Date not in ISO format: {date_str}"
    
    def test_last_updated_not_future_date(self, faq_assistant):
        """Test that last_updated is not in the future."""
        from datetime import datetime
        
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            date_str = result['last_updated']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now()
            
            assert date_obj <= today, \
                f"Date is in future: {date_str}"


class TestMultipleSchemes:
    """Test queries across multiple schemes."""
    
    def test_bluechip_fund_queries(self, faq_assistant):
        """Test multiple Bluechip Fund queries."""
        queries = [
            "What is the expense ratio of SBI Bluechip Fund?",
            "What is the exit load for SBI Bluechip Fund?",
            "Minimum SIP for SBI Bluechip Fund?"
        ]
        
        for query in queries:
            result = faq_assistant.query(query)
            assert result['status'] in ['success', 'no_match', 'refusal', 'error']
    
    def test_different_schemes_queries(self, faq_assistant):
        """Test queries for different schemes."""
        scheme_queries = {
            'Bluechip': 'What is the expense ratio of SBI Bluechip Fund?',
            'Flexicap': 'What is the expense ratio of SBI Flexicap Fund?',
            'ELSS': 'What is the lock-in period for SBI Long Term Equity Fund?',
            'Gilt': 'What are the charges for SBI Magnum Gilt Fund?',
            'Index': 'What is the benchmark for SBI Nifty Index Fund?'
        }
        
        for scheme, query in scheme_queries.items():
            result = faq_assistant.query(query)
            # Should at least get a valid response
            assert 'status' in result


class TestResponseConsistency:
    """Test consistency of responses."""
    
    def test_same_query_same_response(self, faq_assistant):
        """Test that same query returns same response."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        
        result1 = faq_assistant.query(query)
        result2 = faq_assistant.query(query)
        
        # Both should have same status and content
        assert result1['status'] == result2['status']
        if result1['status'] == 'success':
            assert result1['answer'] == result2['answer']
            assert result1['source'] == result2['source']
    
    def test_pii_detection_consistent(self, faq_assistant):
        """Test consistency of PII detection."""
        queries = [
            "My PAN is ABCDE1234F",
            "Account number 123456789",
            "Aadhaar 1234 5678 9012"
        ]
        
        for query in queries:
            results = [faq_assistant.query(query) for _ in range(2)]
            assert results[0]['status'] == results[1]['status'] == 'error'


class TestErrorHandling:
    """Test error handling."""
    
    def test_pii_error_message_informative(self, faq_assistant):
        """Test that PII error message is informative."""
        query = "My PAN is ABCDE1234F"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'error'
        assert 'PAN' in result['message']
        assert 'personal information' in result['message'].lower()
    
    def test_refusal_error_message_helpful(self, faq_assistant):
        """Test that refusal message is helpful."""
        query = "Should I invest in this fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'refusal'
        message = result['message']
        assert 'does not' in message.lower() or 'cannot' in message.lower()
        assert 'amfi' in message.lower() or 'advisor' in message.lower()
    
    def test_no_match_message_helpful(self, faq_assistant):
        """Test that no_match message is helpful."""
        query = "What is quantum mechanics?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'no_match'
        if 'message' in result:
            message = result['message']
            assert 'no matching' in message.lower() or 'not found' in message.lower()


class TestResponseFields:
    """Test that all response fields are present."""
    
    def test_success_response_complete(self, faq_assistant):
        """Test that success response has all fields."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'success':
            assert 'answer' in result
            assert 'source' in result
            assert 'last_updated' in result
    
    def test_error_response_complete(self, faq_assistant):
        """Test that error response has required fields."""
        query = "My PAN is ABCDE1234F"
        result = faq_assistant.query(query)
        
        if result['status'] == 'error':
            assert 'error_type' in result
            assert 'message' in result
    
    def test_refusal_response_complete(self, faq_assistant):
        """Test that refusal response has required fields."""
        query = "Should I invest?"
        result = faq_assistant.query(query)
        
        if result['status'] == 'refusal':
            assert 'error_type' in result
            assert 'message' in result


class TestSpecialCharacters:
    """Test handling of special characters and variations."""
    
    def test_query_with_punctuation(self, faq_assistant):
        """Test query with various punctuation."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert 'status' in result
    
    def test_query_with_extra_spaces(self, faq_assistant):
        """Test query with extra spaces."""
        query = "What   is   the   expense   ratio?"
        result = faq_assistant.query(query)
        
        assert 'status' in result
    
    def test_query_with_special_chars(self, faq_assistant):
        """Test query with special characters."""
        query = "What is the SIP @ minimum?"
        result = faq_assistant.query(query)
        
        assert 'status' in result
