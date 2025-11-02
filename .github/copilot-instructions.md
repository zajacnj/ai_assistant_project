<!-- Updated: 2025-11-02 -->
# VA AI Assistant – Agent Instructions

Concise guidance for AI coding agents working in this Streamlit + SQLite project converted from a Power Apps application.

## 1. Big Picture
Data path: CSV exports (SharePoint lists) → SQLite (`ai_assistant/database/ai_assistant.db`) → Pandas DataFrames → Rendered UI in `main.py`.
Navigation path: Query Params (`?page=...`) override Session State → Page function dispatch → HTML/CSS injection.
Primary screens: `title` → `notice` → `welcome` → `main` (catalog) → `task` / `edit_task` → `help`.

## 2. Core Files
`main.py` – Monolithic app: navigation, styling, page renderers, DB queries, dynamic HTML/JS.
`database_setup.py` – Creates tables (`divisions`, `categories`, `tasks`, `user_tasks`, `user_favorites`). Run after schema changes.
`import_real_data.py` – Loads real SharePoint-exported CSVs in `ai_assistant/data/sharepoint/` into existing tables.
`ai_assistant_setup.py` – Bootstraps directory structure on first run.
`requirements.txt` – Baseline deps (Streamlit, Pandas, Pillow, etc.) plus commented optional integrations.

## 3. Data Access Pattern
Always open DB via `get_database_connection()`; guard with `if conn:`. Query pattern:
```python
conn = get_database_connection()
if conn:
    df = pd.read_sql_query("SELECT * FROM tasks WHERE is_active = 1 ...", conn, params=[...])
    conn.close()
```
Filtering uses LIKE and `%{}%` for division/category; `is_active = 1` is mandatory. Favor extending `load_tasks()` arguments instead of duplicating logic.

## 4. Navigation & State
Query params (`st.query_params`) are authoritative when present; fallback initializes `st.session_state.current_page`. Allowed pages listed in `_allowed_pages`. After changing `st.session_state.current_page` call `st.rerun()`. To add a page: (1) add to `_allowed_pages`, (2) create `show_[name]_page()` implementation, (3) extend dispatch section.

## 5. Styling & Components
Global CSS template near top of `main.py` (variable placeholders filled with `.format`). Images embedded as Base64 via `get_image_as_base64()`. For complex markup isolated in an iframe use `components_html_with_css()` to inject both global and iframe-specific scroll overrides. Keep additions inside existing pattern: define snippet → pass to helper; avoid raw `components.html` duplication.

## 6. Favorites & Lightweight API Actions
## 6. Favorites & Lightweight API Actions
Favoriting implemented by query param API (early exit via api=favt&task=ID param) or inline toggle (favt param). Helper functions toggle_favorite_db and toggle_favorite update the is_favorite column. When extending, keep fast path before page render and use st.stop after response.

## 7. Conventions & Naming
- Page functions follow show_PAGENAME_page pattern from Power Apps heritage
- Data loaders follow load_ENTITY pattern and must filter where is_active equals 1
- All tables include sort_order columns for display ordering
- Template prompt placeholders like `[DATE]` and `[PATIENT_NAME]` are literal - do not transform
- CSS color variables use the --va-COLORNAME naming scheme

## 8. Developer Workflow (Windows)
Initial setup: run `setup.bat` (installs deps, creates structure, builds DB). Manual equivalent:
```bash
pip install -r requirements.txt
python ai_assistant_setup.py
python database_setup.py
streamlit run main.py
```
Import real data: place CSVs in `ai_assistant/data/sharepoint/` then `python import_real_data.py`.
Schema change: edit `database_setup.py` then re-run it; adjust corresponding load function(s).

## 9. Error Handling & Debugging Patterns
All DB ops guarded (`if conn:`); CSS injection wrapped in try/except and falls back to minimal style. For syntax validation use: `py -c "import ast; ast.parse(open('main.py', encoding='utf-8').read())"`. Query param driven actions happen early and may call `st.stop()`. When adding new early handlers keep them above page dispatch and after CSS injection.

## 10. Adding Features Safely
Extend with minimal intrusion: reuse existing CSS template (add placeholders), prefer augmenting `load_tasks()` rather than new query functions. Respect the kiosk-style no-scroll design—if embedding scrollable content use the iframe override pattern found in `components_html_with_css()`. Avoid large refactors without splitting `main.py` (future improvement: migrate pages into `ai_assistant/pages/`).

## 11. Integration Points (Future)
AI services placeholders (OpenAI, Anthropic) are not active; uncomment packages in `requirements.txt` then implement calls in a new helper (e.g., `generate_ai_response(prompt, user_input)`). Authentication planned via `streamlit-authenticator`. Keep these optional so base app runs without secrets.

## 12. Common Pitfalls
Empty catalog: run `database_setup.py` and ensure CSV imports; clear filters (`div=All&cat=All`). Broken navigation: confirm page in `_allowed_pages` and query param presence. Styling anomalies: hard refresh (cache), check that `css_template` format placeholders still match names.

## 13. What Not To Change
Do not remove `is_active` filtering, CSS variable names, or Base64 image approach (avoids external asset dependencies). Preserve query param names (`page`, `div`, `cat`, `q`, `fav`, `mine`, `task`).

---
If any section is unclear or missing context (tests, modularization, deployment), request clarification before large changes.
