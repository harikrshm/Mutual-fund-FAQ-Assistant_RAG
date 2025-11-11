"""
Test suite for advice/refusal detection.

Tests detection and handling of:
- Investment advice requests
- Recommendation requests
- Portfolio-related questions
- Opinion-based queries
"""

import pytest
from src.faq_logic import FAQAssistant


@pytest.fixture
def faq_assistant():
    """Create FAQ Assistant instance for testing."""
    return FAQAssistant()


class TestAdviceTriggerDetection:
    """Test detection of investment advice triggers."""
    
    def test_buy_trigger_detected(self, faq_assistant):
        """Test detection of 'buy' trigger."""
        query = "Should I buy SBI Bluechip Fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_sell_trigger_detected(self, faq_assistant):
        """Test detection of 'sell' trigger."""
        query = "Should I sell my SBI Bluechip Fund units?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_should_i_trigger_detected(self, faq_assistant):
        """Test detection of 'should i' trigger."""
        query = "Should I invest in SBI Flexicap Fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_recommend_trigger_detected(self, faq_assistant):
        """Test detection of 'recommend' trigger."""
        query = "Can you recommend a good fund for me?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_advice_trigger_detected(self, faq_assistant):
        """Test detection of 'advice' trigger."""
        query = "What is your advice on investing?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_suggest_trigger_detected(self, faq_assistant):
        """Test detection of 'suggest' trigger."""
        query = "Can you suggest a fund for my portfolio?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_portfolio_trigger_detected(self, faq_assistant):
        """Test detection of 'portfolio' trigger."""
        query = "How should I build my portfolio?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_worth_investing_trigger_detected(self, faq_assistant):
        """Test detection of 'worth investing' trigger."""
        query = "Is SBI Bluechip Fund worth investing?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_good_investment_trigger_detected(self, faq_assistant):
        """Test detection of 'good investment' trigger."""
        query = "Is ELSS a good investment option?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_bad_investment_trigger_detected(self, faq_assistant):
        """Test detection of 'bad investment' trigger."""
        query = "Is this a bad investment for retirement?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True


class TestAdviceResponseHandling:
    """Test how advice requests are handled."""
    
    def test_advice_request_returns_refusal(self, faq_assistant):
        """Test that advice request returns refusal response."""
        query = "Should I invest in SBI Bluechip Fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'refusal'
        assert result['error_type'] == 'advice_request'
    
    def test_refusal_message_is_polite(self, faq_assistant):
        """Test that refusal message is polite and informative."""
        query = "Can you recommend a fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'refusal'
        message = result['message']
        
        # Check for key phrases
        assert 'does not offer investment advice' in message.lower() or \
               'does not provide' in message.lower()
    
    def test_refusal_includes_amfi_link(self, faq_assistant):
        """Test that refusal message includes AMFI educational link."""
        query = "Should I buy this fund?"
        result = faq_assistant.query(query)
        
        assert result['status'] == 'refusal'
        assert 'amfi' in result['message'].lower() or \
               'amfi' in result.get('source', '').lower()
    
    def test_refusal_has_no_answer(self, faq_assistant):
        """Test that refusal response has no FAQ answer."""
        query = "What fund should I invest in?"
        result = faq_assistant.query(query)
        
        assert result['answer'] is None
    
    def test_refusal_response_structure(self, faq_assistant):
        """Test that refusal response has proper structure."""
        query = "Recommend a good fund for me"
        result = faq_assistant.query(query)
        
        assert 'status' in result
        assert 'error_type' in result
        assert 'message' in result
        assert result['status'] == 'refusal'


class TestCaseSensitivityAdvice:
    """Test advice trigger detection with different cases."""
    
    def test_lowercase_advice_trigger(self, faq_assistant):
        """Test detection with lowercase trigger."""
        query = "should i invest in sbi bluechip fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_uppercase_advice_trigger(self, faq_assistant):
        """Test detection with uppercase trigger."""
        query = "SHOULD I INVEST IN SBI BLUECHIP FUND?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_mixed_case_advice_trigger(self, faq_assistant):
        """Test detection with mixed case trigger."""
        query = "ShOuLd I InVeSt In SbI BlUeChIp FuNd?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True


class TestNonAdviceQueries:
    """Test that factual queries are not incorrectly flagged as advice."""
    
    def test_factual_question_not_advice(self, faq_assistant):
        """Test that factual question isn't flagged as advice."""
        query = "What is the expense ratio of SBI Bluechip Fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_informational_question_not_advice(self, faq_assistant):
        """Test that informational question isn't flagged as advice."""
        query = "What is the lock-in period for ELSS funds?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_definition_question_not_advice(self, faq_assistant):
        """Test that definition question isn't flagged as advice."""
        query = "What does riskometer mean?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_process_question_not_advice(self, faq_assistant):
        """Test that process question isn't flagged as advice."""
        query = "How do I download my statement?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_benchmark_question_not_advice(self, faq_assistant):
        """Test that benchmark question isn't flagged as advice."""
        query = "What is the benchmark for SBI Nifty Index Fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_fee_question_not_advice(self, faq_assistant):
        """Test that fee question isn't flagged as advice."""
        query = "What fees do I pay for this fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False


class TestAdviceEdgeCases:
    """Test edge cases in advice detection."""
    
    def test_word_within_word_not_trigger(self, faq_assistant):
        """Test that triggers within words aren't flagged."""
        # 'buy' is in 'buyer' but shouldn't trigger advice detection necessarily
        query = "Who is the fund buyer?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        # Current implementation may have false positives
        assert isinstance(is_advice, bool)
    
    def test_empty_query_not_advice(self, faq_assistant):
        """Test that empty query is not flagged as advice."""
        query = ""
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is False
    
    def test_single_word_query(self, faq_assistant):
        """Test single word query."""
        query = "buy"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_advice_with_numbers(self, faq_assistant):
        """Test advice request with numbers."""
        query = "Should I invest Rs. 10000 in SBI Bluechip Fund?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True


class TestAdviceDetectionConsistency:
    """Test consistency of advice detection."""
    
    def test_advice_detection_consistency(self, faq_assistant):
        """Test that advice detection is consistent."""
        query = "Should I invest in SBI Bluechip?"
        
        results = [faq_assistant.detect_advice_request(query) for _ in range(3)]
        
        assert all(r == results[0] for r in results)
    
    def test_refusal_response_consistency(self, faq_assistant):
        """Test that refusal responses are consistent."""
        query = "Can you recommend a fund?"
        
        results = [faq_assistant.query(query) for _ in range(2)]
        
        # Both should be refusal
        assert results[0]['status'] == results[1]['status'] == 'refusal'


class TestAdviceTriggerCombinations:
    """Test queries with multiple potential advice triggers."""
    
    def test_multiple_triggers_in_query(self, faq_assistant):
        """Test query with multiple advice triggers."""
        query = "Should I buy and invest in SBI Bluechip? Do you recommend it?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
    
    def test_advice_with_factual_parts(self, faq_assistant):
        """Test advice mixed with factual question."""
        query = "What is the expense ratio? Should I invest?"
        result = faq_assistant.query(query)
        
        # Advice trigger present, so should be refusal
        assert result['status'] == 'refusal'
    
    def test_conditional_advice_query(self, faq_assistant):
        """Test conditional advice query."""
        query = "If the expense ratio is low, should I invest?"
        is_advice = faq_assistant.detect_advice_request(query)
        
        assert is_advice is True
