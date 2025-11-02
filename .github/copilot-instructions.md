# VA AI Assistant - GitHub Copilot Instructions# VA AI Assistant - GitHub Copilot Instructions

<!-- Updated: 2025-10-30 -->

## Project Overview

This is a VA (Veterans Affairs) AI Assistant - a Streamlit web application converted from a Power Apps application. It helps VA employees generate AI prompts for common tasks across different divisions (VHA, VBA, NCA).## Project Overview

This is a **VA (Veterans Affairs) AI Assistant** - a Streamlit web application converted from a Power Apps application. It helps VA employees generate AI prompts for common tasks across different divisions (VHA, VBA, NCA).

## Architecture & Data Flow

```## Architecture & Data Flow

CSV/SharePoint → SQLite Database → Pandas DataFrames → Streamlit UI```

```CSV/SharePoint → SQLite Database → Pandas DataFrames → Streamlit UI

```

**Core Flow**: Page Navigation → Session State → Database Query → Display Results

**Core Flow**: Page Navigation → Session State → Database Query → Display Results

### Key Files Structure

- `main.py` - Main Streamlit app with all screens and navigation logic### Key Files Structure

- `database_setup.py` - Creates SQLite database and schema from sample data  - `main.py` - Main Streamlit app with all screens and navigation logic

- `import_real_data.py` - Imports actual CSV data from SharePoint exports- `database_setup.py` - Creates SQLite database and schema from sample data  

- `ai_assistant_setup.py` - Creates project folder structure- `import_real_data.py` - Imports actual CSV data from SharePoint exports

- `ai_assistant/database/ai_assistant.db` - SQLite database (created by setup)- `ai_assistant_setup.py` - Creates project folder structure

- `ai_assistant/data/sharepoint/` - CSV files exported from SharePoint- `ai_assistant/database/ai_assistant.db` - SQLite database (created by setup)

- `ai_assistant/data/sharepoint/` - CSV files exported from SharePoint

## Navigation Pattern

The app uses **query parameter-driven navigation** with session state fallback:## Navigation Pattern

The app uses **query parameter-driven navigation** with session state fallback:

```python

# Page routing in main.py (around line 1240)```python

requested_page = _get_qp(qp, "page") if qp else None# Page routing in main.py (around line 1240)

_allowed_pages = {"title", "notice", "welcome", "main", "edit_task", "help", "task"}requested_page = _get_qp(qp, "page") if qp else None

if requested_page in _allowed_pages:_allowed_pages = {"title", "notice", "welcome", "main", "edit_task", "help", "task"}

    st.session_state.current_page = requested_pageif requested_page in _allowed_pages:

```    st.session_state.current_page = requested_page

```

**Page Flow**: `title` → `notice` → `welcome` → `main` → `task`/`edit_task`

**Page Flow**: `title` → `notice` → `welcome` → `main` → `task`/`edit_task`

## Database Schema & Data Loading

**Key Tables**: `divisions`, `categories`, `tasks`, `user_tasks`, `user_favorites`## Database Schema & Data Loading

**Key Tables**: `divisions`, `categories`, `tasks`, `user_tasks`, `user_favorites`

**Standard Database Pattern**:

```python**Standard Database Pattern**:

def load_[entity]():```python

    conn = get_database_connection()def load_[entity]():

    if conn:    conn = get_database_connection()

        df = pd.read_sql_query("SELECT * FROM [table] WHERE is_active = 1 ORDER BY sort_order", conn)    if conn:

        conn.close()        df = pd.read_sql_query("SELECT * FROM [table] WHERE is_active = 1 ORDER BY sort_order", conn)

        return df        conn.close()

    return pd.DataFrame()        return df

```    return pd.DataFrame()

```

**Connection**: Always use `get_database_connection()` - handles errors gracefully and connects to `ai_assistant/database/ai_assistant.db`

**Connection**: Always use `get_database_connection()` - handles errors gracefully and connects to `ai_assistant/database/ai_assistant.db`

## CSS & Styling System

The app uses **extensive CSS-in-HTML** with VA design system colors:## CSS & Styling System

The app uses **extensive CSS-in-HTML** with VA design system colors:

**Key VA Colors** (defined around line 70 in main.py):

- va-navy: primary navy blue color**Key VA Colors** (defined around line 70 in main.py):

- va-blue: accent blue color- va-navy: primary navy blue color

- va-gold: highlight gold color- va-blue: accent blue color

- va-gold: highlight gold color

**Image Handling**: SVG/PNG files converted to base64 with `get_image_as_base64()` for embedding in CSS background-image rules.

**Image Handling**: SVG/PNG files converted to base64 with `get_image_as_base64()` for embedding in CSS `background-image` rules.

## Development Workflows

## Development Workflows

### Setup Commands (Windows)

```bash### Setup Commands (Windows)

# One-time setup```bash

setup.bat                    # Installs packages + creates structure + sets up DB# One-time setup

# OR manual:setup.bat                    # Installs packages + creates structure + sets up DB

pip install -r requirements.txt# OR manual:

python ai_assistant_setup.py pip install -r requirements.txt

python database_setup.pypython ai_assistant_setup.py 

python database_setup.py

# Run application  

streamlit run main.py# Run application  

streamlit run main.py

# Import real data

python import_real_data.py   # After placing CSV files in ai_assistant/data/# Import real data

```python import_real_data.py   # After placing CSV files in ai_assistant/data/

```

### Key Development Patterns

### Key Development Patterns

**Add New Screen**:

1. Add page name to `_allowed_pages` list**Add New Screen**:

2. Create `show_[page]_page()` function1. Add page name to `_allowed_pages` list

3. Add routing case in main navigation logic2. Create `show_[page]_page()` function

4. Use `components_html_with_css()` for complex HTML+CSS3. Add routing case in main navigation logic

4. Use `components_html_with_css()` for complex HTML+CSS

**Database Changes**:

1. Modify schema in `database_setup.py`**Database Changes**:

2. Update corresponding `load_[entity]()` function1. Modify schema in `database_setup.py`

3. Test with `python database_setup.py`2. Update corresponding `load_[entity]()` function

3. Test with `python database_setup.py`

**Navigation Links**:

```html**Navigation Links**:

<a href="?page=main">Navigate to Main</a>```html

```<a href="?page=main">Navigate to Main</a>

```

## Project-Specific Conventions

## Project-Specific Conventions

### Error Handling

- Database connections always check `if conn:` before queries### Error Handling

- Image loading uses try/except with fallback to None- Database connections always check `if conn:` before queries

- CSS injection wrapped in try/except with fallback styles- Image loading uses try/except with fallback to None

- CSS injection wrapped in try/except with fallback styles

### Session State Usage

- `st.session_state.current_page` - Primary navigation state### Session State Usage

- `st.session_state.acknowledged` - Notice page acknowledgment- `st.session_state.current_page` - Primary navigation state

- Navigation uses `st.rerun()` after state changes- `st.session_state.acknowledged` - Notice page acknowledgment

- Navigation uses `st.rerun()` after state changes

### PowerApps Migration Context

- Original app was Power Apps with SharePoint backend### PowerApps Migration Context

- Screen names preserve PowerApps naming (e.g., `scrWelcome` → `show_welcome_page()`)- Original app was Power Apps with SharePoint backend

- Reference files in `reference/powerapps_ctx/` contain original app structure- Screen names preserve PowerApps naming (e.g., `scrWelcome` → `show_welcome_page()`)

- CSV files maintain SharePoint column names and schema- Reference files in `reference/powerapps_ctx/` contain original app structure

- CSV files maintain SharePoint column names and schema

## Common Debugging

- **Database errors**: Check if `python database_setup.py` was run## Common Debugging

- **Missing images**: Verify files exist in `ai_assistant/images/`- **Database errors**: Check if `python database_setup.py` was run

- **CSS issues**: Check `components_html_with_css()` usage vs `st.markdown()`- **Missing images**: Verify files exist in `ai_assistant/images/`

- **Navigation issues**: Verify page name in `_allowed_pages` and routing logic- **CSS issues**: Check `components_html_with_css()` usage vs `st.markdown()`

- **Syntax errors**: Use `py -c "import ast; ast.parse(open('main.py', encoding='utf-8').read())"` to validate syntax- **Navigation issues**: Verify page name in `_allowed_pages` and routing logic

- **Function structure**: Check for incomplete try/except blocks and missing function closures- **Syntax errors**: Use `py -c "import ast; ast.parse(open('main.py', encoding='utf-8').read())"` to validate syntax

- **Function structure**: Check for incomplete try/except blocks and missing function closures

## Integration Points

- **SharePoint**: CSV export → Python import workflow via `import_real_data.py`## Integration Points

- **AI Services**: Placeholder integration points in PROJECT_SUMMARY.md for ChatGPT/Claude- **SharePoint**: CSV export → Python import workflow via `import_real_data.py`

- **Authentication**: Future integration points documented but not implemented- **AI Services**: Placeholder integration points in PROJECT_SUMMARY.md for ChatGPT/Claude
- **Authentication**: Future integration points documented but not implemented