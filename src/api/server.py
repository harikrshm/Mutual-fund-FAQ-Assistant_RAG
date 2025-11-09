"""
Flask API server for FAQ Assistant
Provides REST API endpoint for FAQ queries
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add parent directory to path to import faq_logic
sys.path.insert(0, str(Path(__file__).parent.parent))

from faq_logic import FAQAssistant

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize FAQ Assistant
assistant = FAQAssistant()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/query', methods=['POST'])
def query():
    """Query FAQ endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'error_type': 'invalid_request',
                'message': 'Query is required'
            }), 400
        
        query_text = data['query']
        
        if not isinstance(query_text, str) or not query_text.strip():
            return jsonify({
                'status': 'error',
                'error_type': 'invalid_request',
                'message': 'Query must be a non-empty string'
            }), 400
        
        # Process query
        result = assistant.query(query_text)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error processing query: {e}", file=sys.stderr)
        return jsonify({
            'status': 'error',
            'error_type': 'server_error',
            'message': 'An error occurred while processing your query'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

