Tasks

 0.0 Create feature branch

 0.1 Create and checkout a new branch for this feature (e.g., git checkout -b feature/mutual-fund-faq-assistant)

 0.2 Push the branch to origin (git push -u origin feature/mutual-fund-faq-assistant)

 1.0 Define Scope and Corpus

 1.1 Choose one AMC (e.g., Axis Mutual Fund / SBI Mutual Fund / ICICI Prudential).

 1.2 Select 3–5 schemes across categories (Large-cap, Flexi-cap, ELSS, optional Debt/Index).

 1.3 Create src/config.yml with amc_name, schemes: [], and basic metadata.

 1.4 Create README.md section “Scope” listing the chosen AMC & schemes.

 1.5 Add a short note about known limits (static snapshots, not real-time NAVs).

 2.0 Collect and Organize Official Data Sources (15–25 URLs)

 2.1 Identify official domains to use (AMC official site, AMFI, SEBI).

 2.2 For each selected scheme, download/record Factsheet, KIM/SID, and any scheme-specific FAQ or fees page. Save URLs and file names in src/data/sources.csv.

 2.3 Collect general guidance pages (AMFI how-to, SEBI disclosure, AMC statement-download guide).

 2.4 Validate each source domain with src/utils/validate_sources.py (script to check domain whitelist).

 2.5 Ensure 15–25 total entries; mark source type (factsheet, KIM, FAQ, gov guide) in CSV.

 2.6 Note date_accessed for each entry (use ISO format YYYY-MM-DD).

 3.0 Build FAQ Dataset (JSON/CSV)

 3.1 Define canonical question templates to cover required facts (expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, how to download statements).

 3.2 Create src/data/faqs.json schema:

{
  "q_key": {
    "question_variants": ["Expense ratio of Axis Bluechip Fund", "What is the expense ratio?"],
    "answer": "Direct plan expense ratio: 0.62%.",
    "source": "https://example.com/factsheet.pdf",
    "last_updated": "2025-10-01"
  }
}


 3.3 Populate the dataset for all selected schemes — target 50–80 Q&A pairs covering variations.

 3.4 Add sample_faqs/sample_faq.csv with 5–10 example queries + expected app output (for demo).

 3.5 Run a small QA validation script (src/utils/qa_validate.py) to ensure every entry has a source and last_updated.

 4.0 Implement Prototype UI from Figma  
  > **Context:** You will provide the Figma link/design for the existing web UI. This task implements that UI faithfully (visual tokens, components, spacing, interactions), and integrates the FAQ logic so the app behaves as the design specifies.

  - [ ] 4.1 Add the Figma link: create `design/figma-link.txt` and paste the share URL you provide.  
  - [ ] 4.2 Inspect Figma and create a design mapping document `design/figma-mapping.md` that lists:
    - UI screens and routes (e.g., Home, Query, Results, About),
    - Components to implement (Header, QueryBox, ExamplesList, ResultCard, SourceLink, DisclaimerBanner, Footer),
    - Visual tokens (colors, typography, spacing, border radii, shadows),
    - Interaction notes (hover/focus states, transitions, microcopy).
  - [ ] 4.3 Export assets from Figma into `design/assets/` (SVG icons, PNGs for avatars, exported images). Capture asset sizes and usage notes in `design/figma-mapping.md`.
  - [ ] 4.4 Generate design tokens:
    - Create `src/web/styles/tokens.css` or `src/web/styles/tokens.json` with color variables, font sizes, and spacing derived from Figma.
    - If using Tailwind, create `src/web/styles/tailwind.config.js` mapping tokens to the Tailwind config.
  - [ ] 4.5 Implement frontend components to match Figma:
    - `src/web/components/Header.tsx` – exact spacing and typography as Figma header.
    - `src/web/components/QueryBox.tsx` – input box, placeholder, example chips, and keyboard states.
    - `src/web/components/ResultCard.tsx` – answer layout (≤3 sentences), single source link, "Last updated" line, and optional "Show source details" toggle.
    - `src/web/components/DisclaimerBanner.tsx` – persistent banner with exact copy from `disclaimer.txt`.
    - Ensure components are modular and documented with story-like examples.
  - [ ] 4.6 Implement responsive breakpoints and test in desktop/tablet/mobile canvas to match Figma frames. Document where responsive behavior differs (if any) in `design/notes_responsive.md`.
  - [ ] 4.7 Implement interactions & micro-animations defined in Figma:
    - Hover/focus states,
    - Input validation states (error for PII),
    - Result loading skeletons,
    - Source link opening (open in new tab).
  - [ ] 4.8 Integrate frontend with backend FAQ logic:
    - Hook `src/web` to `src/faq_logic.py` via an API route `src/web/api/query` or by embedding the logic directly for desktop prototypes.
    - Ensure responses returned to the UI follow the format: `{ answer: string, source: string, last_updated: string }`.
  - [ ] 4.9 Accessibility & QA:
    - Ensure components have appropriate aria labels, keyboard navigation, color contrast per WCAG AA.
    - Add automated accessibility checks (axe or similar) in CI or run locally.
  - [ ] 4.10 Pixel QA and handoff:
    - Use a pixel-compare checklist to validate Figma vs implementation for key screens.
    - Capture screenshots for differences and log any accepted deviations.
  - [ ] 4.11 Tests & E2E:
    - Add visual regression tests if possible (Percy or jest-image-snapshot).
    - Add E2E tests (Cypress / Playwright) that simulate a user query, assert that answer is ≤3 sentences and that the single source link and "Last updated" appear.

- [ ] 5.0 Create UI and Add Compliance Elements (moved/updated to reflect Figma-driven UI)  
  - [ ] 5.1 Place the disclaimer snippet in `disclaimer.txt` and ensure the `DisclaimerBanner` matches Figma placement.  
  - [ ] 5.2 Implement PII detection in the frontend (prevent submission) and backend (additional guard). Show an inline error messageonsistent with Figma error styling.  
  - [ ] 5.3 Add a "View Source" toggle/action that reveals the single source URL and `date_accessed` (UI placement per Figma).  
  - [ ] 5.4 Implement the “refuse opinionated/portfolio questions” UI state per the design: show polite refusal copy + a link to educational resources (e.g., AMFI).  
  - [ ] 5.5 Ensure logs exclude PII; if a user attempts to paste PII, the UI should block and not transmit it to the server.



 6.0 Documentation, Tests, and Submission Prep

 6.1 Write README.md: setup, run, scope (AMC + schemes), known limits (static snapshot, not advice), and how to update sources/faqs.

 6.2 Provide sources.csv and sample_faq.csv in the repo root (or /src/data/).

 6.3 Create test coverage for code paths: matching, refusal, PII detection (pytest tests).

 6.4 Record a ≤3-minute demo video or host the app and produce working prototype link. Add link/path to README.

 6.5 Final checklist: confirm every answer includes exactly one source link, answers ≤3 sentences, disclaimer visible, and no PII is accepted or stored.

 6.6 Tag the branch for review (git tag -a v0.1-mf-faq -m "Mutual Fund FAQ assistant prototype").

 7.0 Review & Handover

 7.1 Peer review: request review and address feedback.

 7.2 Merge feature branch to develop/main as per project workflow.

 7.3 Deliver final submission package (README, src/, src/data/, demo/, tests/) and ensure tasks/ file is up-to-date.

 7.4 Archive / document known edge cases and next steps (e.g., automation to refresh factsheets).

Relevant Implementation Details & Quick Commands

Create branch:

git checkout -b feature/mutual-fund-faq-assistant
git push -u origin feature/mutual-fund-faq-assistant


Run Streamlit demo locally:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py


Run tests:

pytest -q

Deliverables Checklist (for submission)

 Working prototype link (app or notebook) or ≤3-min demo video.

 src/data/sources.csv (15–25 official URLs).

 src/data/faqs.json (structured Q&A).

 sample_faqs/sample_faq.csv (5–10 sample Q&A).

 README.md (setup, scope, known limits).

 disclaimer.txt (UI disclaimer snippet).

 Tests and CI scripts.

Disclaimer Snippet (copy into disclaimer.txt)

Facts-only. No investment advice. This assistant only provides factual information drawn from official AMC / AMFI / SEBI public pages. It does not offer investment advice, recommendations, or portfolio suggestions. Always verify critical details from the original scheme documents linked in each response.