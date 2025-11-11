# Mutual Fund FAQ Assistant (RAG)

A fact-only FAQ assistant that answers factual questions about mutual fund schemes using only official public pages. The assistant covers expense ratios, exit loads, minimum SIP amounts, lock-in periods (ELSS), riskometer ratings, benchmarks, and statement download procedures. **Every answer includes exactly one source link. No investment advice is provided.**

## Table of Contents

- [Scope](#scope)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Known Limits](#known-limits)
- [Compliance & Safety](#compliance--safety)
- [Updating FAQ Data](#updating-faq-data)
- [Project Structure](#project-structure)
- [Testing](#testing)

## Scope

### Covered AMC
- **SBI Mutual Fund**

### Covered Schemes

This FAQ assistant provides factual information for 5 SBI Mutual Fund schemes across different categories:

1. **SBI Bluechip Fund** - Large-cap equities
2. **SBI Flexicap Fund** - Flexible large-cap equities
3. **SBI Long Term Equity Fund** - ELSS (tax-saving) equity fund
4. **SBI Magnum Gilt Fund** - Debt (government securities)
5. **SBI Nifty Index Fund** - Index fund tracking Nifty 50

### Covered Topics

- Expense Ratio (direct vs. regular plans)
- Exit Load / Early Withdrawal Charges
- Minimum Investment & SIP Amounts
- Lock-in Period (especially for ELSS)
- Riskometer Rating
- Benchmark Index
- How to Download Statements

## Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/harikrshm/Mutual-fund-FAQ-Assistant_RAG.git
cd Mutual-fund-FAQ-Assistant_RAG
```

### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `flask`: Web framework for the API server
- `flask-cors`: Cross-Origin Resource Sharing support
- Additional dependencies as needed

### 4. Verify Installation

```bash
python -c "import flask; print('Flask installed successfully')"
```

## Running the Application

### Option 1: Run the Flask API Server

Start the backend API server that serves FAQ queries:

```bash
python src/api/server.py
```

The API will be available at `http://localhost:5000`.

**Example API call:**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the expense ratio of SBI Bluechip Fund?"}'
```

**Expected response:**
```json
{
  "answer": "The direct plan expense ratio for SBI Bluechip Fund is approximately 0.62%...",
  "source": "https://www.sbmf.com/schemes/bluechip/factsheet.pdf",
  "last_updated": "2025-01-09",
  "status": "success"
}
```

### Option 2: Run Tests

Execute the test suite to validate functionality:

```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=src tests/
```

### Option 3: Interactive Python Usage

Query the FAQ system directly from Python:

```python
from src.faq_logic import FAQAssistant

assistant = FAQAssistant()
query = "What is the minimum SIP for SBI Bluechip Fund?"

has_pii, pii_types = assistant.detect_pii(query)
if has_pii:
    print(f"PII detected: {pii_types}")
else:
    result = assistant.query(query)
    print(result)
```

## Demo & Examples

### Live Queries

The following queries showcase the FAQ Assistant's capabilities:

**Factual Query:**
```bash
Query: "What is the expense ratio of SBI Bluechip Fund?"
Expected: Returns expense ratio with source link
```

**ELSS-Specific Query:**
```bash
Query: "What is the lock-in period for SBI Long Term Equity Fund?"
Expected: Returns 3-year lock-in information with source
```

**Investment Advice (Refused):**
```bash
Query: "Should I invest in SBI Bluechip Fund?"
Expected: Polite refusal + link to AMFI educational resources
```

**PII Detection (Blocked):**
```bash
Query: "What is the expense ratio? My PAN is ABCDE1234F"
Expected: Error response stating PII detected
```

### Sample FAQ Queries

A comprehensive set of sample queries with expected outputs is available in:
- **File:** `sample_faqs/sample_faq.csv` (10 pre-tested queries)

### Prototype Status

**Version:** v0.1-mf-faq (Prototype)
- **Status:** Static data snapshot from January 2025
- **Test Coverage:** Full pytest suite covering:
  - FAQ matching (150+ test cases)
  - PII detection (80+ test cases)
  - Investment advice refusal (50+ test cases)
  - Integration tests (40+ test cases)
- **Running Tests:** `pytest -v` (320+ assertions total)

## Known Limits

### 1. Static Snapshots
- This assistant provides information based on **static snapshots** of official documents at the time of collection (January 2025).
- Data is **not updated in real-time**.
- New scheme features, expense ratio changes, or policy updates made after collection date are not reflected.

### 2. No Real-Time NAVs
- The assistant does **not** provide real-time Net Asset Values (NAVs) or current market data.
- For current NAVs, always visit the official SBI Mutual Fund website.

### 3. Historical Data Only
- All information is derived from official documents (factsheets, Key Information Memoranda / Scheme Information Documents) that were available at the time of data collection.
- Past performance or historical benchmarks are included only if present in source documents.

### 4. Limited to Factual Questions
- The assistant **refuses** investment advice, recommendations, or portfolio suggestions.
- Opinionated questions (e.g., "Should I invest in...?") will receive a polite refusal with a link to AMFI educational resources.

### 5. English Language Only
- All queries and responses are in English.

### 6. No PII Storage
- The assistant detects and **rejects** personally identifiable information (PAN, Aadhaar, account numbers).
- No user queries are stored in logs.

## Compliance & Safety

### Disclaimer

**Facts-only. No investment advice.** This assistant only provides factual information drawn from official AMC / AMFI / SEBI public pages. It does not offer investment advice, recommendations, or portfolio suggestions. Always verify critical details from the original scheme documents linked in each response.

### PII Detection

The system detects and blocks the following:
- **PAN** (Personal Account Number): 10-digit format
- **Aadhaar**: 12-digit format
- **Account Numbers**: 9–18 digit sequences

### Quality Assurance

- **Answer Quality**: Every answer is ≤3 sentences and directly sourced.
- **Source Inclusion**: Every response includes exactly one source link.
- **Last Updated**: Every response includes a last updated timestamp.
- **Refusal Handling**: Advice requests are politely refused with educational resources.

## Updating FAQ Data

### Adding New FAQs

1. **Edit or expand `src/data/faqs.json`:**

```json
{
  "new_scheme_key": {
    "question_variants": [
      "How do I open an account?",
      "Can I open a new account for this scheme?"
    ],
    "answer": "You can open an account by visiting the official SBI Mutual Fund website or contacting an authorized distributor.",
    "source": "https://www.sbmf.com/how-to-invest",
    "last_updated": "2025-01-09",
    "scheme_name": "SBI Bluechip Fund",
    "category": "account_opening"
  }
}
```

2. **Update sources in `src/data/sources.csv`:**

Add a new row with:
- `url`: Official source URL
- `file_name`: Document name (e.g., "bluechip_factsheet_2025.pdf")
- `source_type`: One of `factsheet`, `kim`, `faq`, `gov_guide`, `scheme_page`
- `date_accessed`: ISO format (YYYY-MM-DD)

3. **Validate changes:**

```bash
python src/utils/qa_validate.py
python src/utils/validate_sources.py
```

4. **Test your changes:**

```bash
pytest tests/test_faq_logic.py -v
```

### Schema Requirements

Every FAQ entry must have:
- `question_variants`: List of at least 2 question phrasings
- `answer`: ≤3 sentences
- `source`: Valid URL to official document
- `last_updated`: ISO date (YYYY-MM-DD)
- `scheme_name`: Name of the scheme (for filtering)
- `category`: Topic category (e.g., "expense_ratio", "exit_load")

### Refreshing Data

To refresh data from official sources:

1. Visit official SBI Mutual Fund pages and AMFI resources
2. Download latest factsheets and KIM documents
3. Update URLs in `src/data/sources.csv`
4. Refresh Q&A content in `src/data/faqs.json`
5. Run validation:
   ```bash
   python src/utils/qa_validate.py
   ```
6. Commit changes with a descriptive message

## Project Structure

```
Mutual-fund-FAQ-Assistant_RAG/
├── README.md                    # This file
├── disclaimer.txt               # Compliance disclaimer
├── requirements.txt             # Python dependencies
├── src/
│   ├── config.yml              # AMC and scheme configuration
│   ├── faq_logic.py            # Core FAQ matching logic
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py           # Flask API server
│   ├── data/
│   │   ├── faqs.json           # FAQ database
│   │   └── sources.csv         # Source document URLs
│   ├── utils/
│   │   ├── qa_validate.py      # FAQ data validation
│   │   ├── pii_detection.py    # PII detection utilities
│   │   └── validate_sources.py # Source URL validation
│   └── web/
│       ├── components/         # React/Next.js components
│       ├── pages/             # Page routes
│       ├── styles/            # CSS and design tokens
│       ├── utils/             # Frontend utilities
│       ├── tests/             # Component & unit tests
│       └── e2e/               # End-to-end tests (Playwright)
├── sample_faqs/
│   └── sample_faq.csv         # Example queries for demo
├── tests/
│   └── test_*.py              # pytest test suite
└── design/
    ├── figma-link.txt         # Figma design URL
    ├── figma-mapping.md       # Design specs and tokens
    └── assets/                # Design exports
```

## Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Modules

```bash
# Test FAQ matching logic
pytest tests/test_faq_logic.py -v

# Test PII detection
pytest tests/test_pii_detection.py -v

# Test refusal logic
pytest tests/test_refusal.py -v
```

### Coverage Report

```bash
pytest --cov=src --cov-report=html tests/
# Opens htmlcov/index.html in your browser
```

### Test Categories

- **Functional Tests**: FAQ matching, PII detection, advice refusal
- **Integration Tests**: API server endpoints
- **Component Tests**: React/Next.js components (Jest)
- **E2E Tests**: Full user workflows (Playwright)

## Version & Release Info

- **Version**: v0.1-mf-faq
- **Release Date**: January 2025
- **Status**: Prototype (static data snapshot)
- **Tag**: `v0.1-mf-faq` - Use `git checkout v0.1-mf-faq` to access this release

## License

[License information to be added]

## Contributing

For updates, bug reports, or new FAQs, please create an issue or submit a pull request with:
1. Updated `src/data/faqs.json` entries
2. Updated `src/data/sources.csv` if adding new official sources
3. Test cases validating the changes
4. Any modified utility scripts

## Support & Contact

For questions or feedback about this FAQ assistant, please contact the development team.