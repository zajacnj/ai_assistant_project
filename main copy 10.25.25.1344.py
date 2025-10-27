"""
VA AI Assistant - Updated with Official SVG VA Seal
Uses the high-quality SVG version of the Department of Veterans Affairs seal
"""

import streamlit as st
import sqlite3
import pandas as pd
import time
import base64
from datetime import datetime
from PIL import Image
import os
import textwrap
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="VA AI Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DEBUG banner removed — normal startup proceeds

# Helper function to load and encode images
def get_image_as_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        if os.path.exists(image_path):
            if image_path.endswith('.svg'):
                # SVG files are text-based
                with open(image_path, "r", encoding="utf-8") as img_file:
                    svg_content = img_file.read()
                    return base64.b64encode(svg_content.encode('utf-8')).decode()
            else:
                # Binary files like PNG, JPG
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except:
        pass
    return None

# Load VA images - prioritize SVG seal
va_seal_b64 = get_image_as_base64("ai_assistant/images/Seal_of_the_U.S._Department_of_Veterans_Affairs.svg")
vha_icon_b64 = get_image_as_base64("ai_assistant/images/VHA.png")
vba_icon_b64 = get_image_as_base64("ai_assistant/images/VBA.png")
nca_icon_b64 = get_image_as_base64("ai_assistant/images/NCA.png")
admin_icon_b64 = get_image_as_base64("ai_assistant/images/Administrative.png")
edu_icon_b64 = get_image_as_base64("ai_assistant/images/Education.png")
finance_icon_b64 = get_image_as_base64("ai_assistant/images/Finance.png")
hr_icon_b64 = get_image_as_base64("ai_assistant/images/Human Resources.png")
it_icon_b64 = get_image_as_base64("ai_assistant/images/IT.png")
mgmt_icon_b64 = get_image_as_base64("ai_assistant/images/Management.png")
medical_icon_b64 = get_image_as_base64("ai_assistant/images/Medical.png")
qps_icon_b64 = get_image_as_base64("ai_assistant/images/QPS.png")

# Build optional background rules (safe strings)
va_logo_bg = ("background-image: url(data:image/svg+xml;base64," + va_seal_b64 + ");") if va_seal_b64 else ""
va_seal_bg = va_logo_bg
header_logo_icon_bg = va_logo_bg

vha_icon_rule = ("background-image: url(data:image/png;base64," + vha_icon_b64 + ");") if vha_icon_b64 else ""
vba_icon_rule = ("background-image: url(data:image/png;base64," + vba_icon_b64 + ");") if vba_icon_b64 else ""
nca_icon_rule = ("background-image: url(data:image/png;base64," + nca_icon_b64 + ");") if nca_icon_b64 else ""
admin_icon_rule = ("background-image: url(data:image/png;base64," + admin_icon_b64 + ");") if admin_icon_b64 else ""
edu_icon_rule = ("background-image: url(data:image/png;base64," + edu_icon_b64 + ");") if edu_icon_b64 else ""
finance_icon_rule = ("background-image: url(data:image/png;base64," + finance_icon_b64 + ");") if finance_icon_b64 else ""
hr_icon_rule = ("background-image: url(data:image/png;base64," + hr_icon_b64 + ");") if hr_icon_b64 else ""
it_icon_rule = ("background-image: url(data:image/png;base64," + it_icon_b64 + ");") if it_icon_b64 else ""
mgmt_icon_rule = ("background-image: url(data:image/png;base64," + mgmt_icon_b64 + ");") if mgmt_icon_b64 else ""
medical_icon_rule = ("background-image: url(data:image/png;base64," + medical_icon_b64 + ");") if medical_icon_b64 else ""
qps_icon_rule = ("background-image: url(data:image/png;base64," + qps_icon_b64 + ");") if qps_icon_b64 else ""

# CSS template uses doubled braces for literal CSS braces and single braces for placeholders.
css_template = """
<style>
    /* Load Open Sans */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');

    html, body, .main, .block-container {{
        font-family: 'Open Sans', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    *, *::before, *::after {{ box-sizing: inherit; }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}

    .main {{
        padding: 0 !important;
        margin: 0 !important;
    }}

    .block-container {{
        padding: 1rem !important;
        max-width: none !important;
    }}

    :root {{
        --va-navy: #111D42;
        --va-blue: #0071bc;
        --va-light-blue: #9bdaf1;
        --va-gold: #fdb81e;
        --va-orange: #e31c3d;
        --va-green: #2e8540;
        --va-gray: #5b616b;
        --va-gray-light: #aeb0b5;
        --va-gray-lighter: #d6d7d9;
        --va-gray-lightest: #f1f1f1;
    }}

    .title-page {{
        background: linear-gradient(135deg, var(--va-navy) 0%, #1e3a8a 100%);
        color: white;
        text-align: center;
        padding: clamp(1rem, 3vw, 3.5rem) 1.5rem;
        height: calc(100vh - 2rem);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }}

    .va-logo-large {{
        width: clamp(160px, 20vw, 250px);
        height: clamp(160px, 20vw, 250px);
        background: white;
        border-radius: 50%;
        margin: 0 auto 3rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        position: relative;
        {va_logo_bg}
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .title-main {{
        font-size: clamp(2.4rem, 6vw, 4.5rem);
        font-weight: 300;
        margin-bottom: 1rem;
        letter-spacing: 2px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        line-height: 1.05;
    }}

    .title-subtitle {{
        font-size: clamp(1rem, 2.2vw, 1.8rem);
        opacity: 0.95;
        font-style: italic;
        font-weight: 300;
        margin-top: 0.5rem;
    }}

    .version-badge {{
        position: absolute;
        /* keep badge inside the viewport to avoid overflow */
        bottom: 1.25rem;
        right: 1.25rem;
        background: var(--va-green);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}

    /* ============ NOTICE PAGE ============ */
    /* size to viewport so page fits without scrollbars */
    .notice-page {{
        background: var(--va-gray-lightest);
        height: calc(100vh - 2rem);
        padding: 1.25rem 0;
        margin: -1rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .notice-container {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid var(--va-gray-lighter);
        max-width: 1000px;
        width: 100%;
        margin: 0 2rem;
    }}

    .notice-header {{
        color: var(--va-orange);
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-align: center;
    }}

    .notice-subtitle {{
        font-size: 1.2rem;
        color: var(--va-gray);
        margin-bottom: 2rem;
        text-align: center;
    }}

    .notice-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        column-gap: 2rem;
        row-gap: 1.5rem; /* vertical spacing between pairs */
        margin-bottom: 2rem;
        text-align: left;
    }}

    .notice-item {{
        background: var(--va-gray-lightest);
        border-radius: 15px;
        padding: 1.5rem;
        /* removed left border to eliminate black edge */
        border-left: none;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }}

    /* spacing controlled by grid gaps; no extra side margins required */

    .notice-icon {{
        width: 50px;
        height: 50px;
        background: var(--va-navy);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(17,46,81,0.3);
    }}

    .notice-content h4 {{
        color: var(--va-navy);
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: bold;
    }}

    .notice-content p {{
        color: var(--va-gray);
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }}

    .notice-acknowledge {{
        text-align: center;
        margin-top: 1rem;
    }}

    /* style the anchor used as the acknowledge button when rendering in main DOM */
    .ack-link {{
        display: inline-block;
        background: var(--va-navy);
        color: white;
        padding: 12px 36px;
        border-radius: 12px;
        font-weight: 700;
        text-decoration: none;
        box-shadow: 0 8px 20px rgba(17,46,81,0.25);
    }}

    /* ============ WELCOME PAGE ============ */
    .welcome-page {{
        min-height: 100vh;
        padding: 0;
        margin: -1rem;
        background: var(--va-gray-lightest);
        display: flex;
        align-items: center;
    }}

    .welcome-left {{
        flex: 1;
        background: var(--va-navy);
        color: white;
        padding: 4rem 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: 100vh;
        position: relative;
        background: linear-gradient(45deg, var(--va-navy) 0%, #1e3a8a 100%);
    }}

    .va-seal {{
        width: 320px;
        height: 320px;
        background: white;
        border-radius: 50%;
        margin-bottom: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        {va_seal_bg}
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .welcome-title {{
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}

    .welcome-subtitle {{
        font-size: 1.3rem;
        opacity: 0.95;
        font-style: italic;
        font-weight: 300;
    }}

    .welcome-right {{
        flex: 1;
        background: white;
        padding: 4rem 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100vh;
    }}

    .welcome-content h2 {{
        color: var(--va-gray);
        font-size: 3rem;
        font-weight: 300;
        margin-bottom: 2rem;
        text-align: center;
    }}

    .welcome-content p {{
        color: var(--va-gray);
        font-size: 1.2rem;
        line-height: 1.6;
        margin-bottom: 3rem;
        text-align: center;
    }}

    .template-count {{
        color: var(--va-gray-light);
        font-size: 1.1rem;
        font-style: italic;
        text-align: center;
        margin-top: 2rem;
    }}

    /* ============ MAIN INTERFACE ============ */
    .main-header {{
        background: var(--va-navy);
        color: white;
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .header-logo {{
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 1.5rem;
        font-weight: bold;
    }}

    .header-logo-icon {{
        width: 40px;
        height: 40px;
        background: white;
        color: var(--va-navy);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        {header_logo_icon_bg}
        background-size: 35px 35px;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Custom buttons styling */
    .stButton > button {{
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        border: 1px solid var(--va-gray-lighter) !important;
        background: white !important;
        color: var(--va-gray) !important;
    }}

    .stButton > button:hover {{
        background: var(--va-light-blue) !important;
        border-color: var(--va-blue) !important;
        color: var(--va-navy) !important;
        transform: translateX(2px) !important;
    }}

    /* Task cards */
    .task-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid var(--va-gray-lighter);
        transition: all 0.3s ease;
    }}

    .task-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        border-color: var(--va-blue);
    }}

    .task-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }}

    .task-title {{
        color: var(--va-navy);
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0;
        flex: 1;
        line-height: 1.3;
    }}

    .task-favorite {{
        font-size: 1.5rem;
        margin-left: 1rem;
    }}

    .task-description {{
        color: var(--va-gray);
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }}

    .task-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid var(--va-gray-lighter);
    }}

    .task-category {{
        background: var(--va-light-blue);
        color: var(--va-navy);
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
    }}

    .task-arrow {{
        color: var(--va-navy);
        font-size: 1.2rem;
    }}

    /* Division and category button styling */
    .division-btn, .category-btn {{
        background: white;
        border: 1px solid var(--va-gray-lighter);
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 8px;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s ease;
        cursor: pointer;
        font-size: 14px;
        color: var(--va-gray);
    }}

    .division-btn:hover, .category-btn:hover {{
        background: var(--va-light-blue);
        border-color: var(--va-blue);
        color: var(--va-navy);
        transform: translateX(2px);
    }}

    .btn-icon {{
        width: 35px;
        height: 35px;
        background-size: 30px 30px;
        background-position: center;
        background-repeat: no-repeat;
        background-color: var(--va-gray-lightest);
        border-radius: 8px;
        flex-shrink: 0;
    }}

    /* Specific icon classes with base64 images */
    .vha-icon {{ {vha_icon_rule} }}
    .vba-icon {{ {vba_icon_rule} }}
    .nca-icon {{ {nca_icon_rule} }}
    .administrative-icon {{ {admin_icon_rule} }}
    .education-icon {{ {edu_icon_rule} }}
    .finance-icon {{ {finance_icon_rule} }}
    .hr-icon {{ {hr_icon_rule} }}
    .it-icon {{ {it_icon_rule} }}
    .management-icon {{ {mgmt_icon_rule} }}
    .medical-icon {{ {medical_icon_rule} }}
    .qps-icon {{ {qps_icon_rule} }}

    @media (max-width: 1200px) {{
        .welcome-page {{
            flex-direction: column;
        }}
        .welcome-left, .welcome-right {{
            flex: none;
            min-height: 50vh;
        }}
        .notice-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    @media (max-width: 768px) {{
        .title-main {{ font-size: 2.5rem; }}
        .welcome-title {{ font-size: 2rem; }}
        .va-seal {{ width: 250px; height: 250px; }}
        .notice-container {{ padding: 2rem; margin: 0 1rem; }}
    }}
</style>
"""

# Render final CSS by filling placeholders
css_styles = css_template.format(
    va_logo_bg=va_logo_bg,
    va_seal_bg=va_seal_bg,
    header_logo_icon_bg=header_logo_icon_bg,
    vha_icon_rule=vha_icon_rule,
    vba_icon_rule=vba_icon_rule,
    nca_icon_rule=nca_icon_rule,
    admin_icon_rule=admin_icon_rule,
    edu_icon_rule=edu_icon_rule,
    finance_icon_rule=finance_icon_rule,
    hr_icon_rule=hr_icon_rule,
    it_icon_rule=it_icon_rule,
    mgmt_icon_rule=mgmt_icon_rule,
    medical_icon_rule=medical_icon_rule,
    qps_icon_rule=qps_icon_rule
)

# Inject the CSS into the main Streamlit document so st.markdown(...) HTML uses it
try:
    st.markdown(css_styles, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to inject global CSS: {e}")
    css_styles = "<style>html,body{font-family: Arial, sans-serif;}</style>"
    st.markdown(css_styles, unsafe_allow_html=True)

def components_html_with_css(inner_html: str, height: int = 600, scrolling: bool = True):
    """
    Render HTML inside Streamlit components with the same css_styles injected
    so the iframe gets the styling. Fail gracefully and show error output.
    """
    full_html = css_styles + "\n" + textwrap.dedent(inner_html)
    try:
        return components.html(full_html, height=height, scrolling=scrolling)
    except Exception as e:
        st.error(f"components.html failed: {e}")
        # show the raw HTML as text to help debugging
        st.code(full_html[:1000] + ("..." if len(full_html) > 1000 else ""), language="html")
        return None

def get_database_connection():
    """Connect to the SQLite database"""
    try:
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def load_divisions():
    """Load divisions from database"""
    conn = get_database_connection()
    if conn:
        df = pd.read_sql_query("SELECT * FROM divisions WHERE is_active = 1 ORDER BY sort_order", conn)
        conn.close()
        return df
    return pd.DataFrame()

def load_categories(division=None):
    """Load categories from database"""
    conn = get_database_connection()
    if conn:
        if division and division != "All":
            df = pd.read_sql_query(
                "SELECT * FROM categories WHERE is_active = 1 AND division LIKE ? ORDER BY sort_order",
                conn, params=["%{}%".format(division)]
            )
        else:
            df = pd.read_sql_query("SELECT * FROM categories WHERE is_active = 1 ORDER BY sort_order", conn)
        conn.close()
        return df
    return pd.DataFrame()

def load_tasks(task_id=None, division=None, category=None, search_term="", show_favorites=False, show_user_tasks=False):
    """Load tasks from database with filters. If task_id is provided, return that task."""
    conn = get_database_connection()
    if conn:
        try:
            if task_id is not None:
                df = pd.read_sql_query(
                    "SELECT * FROM tasks WHERE task_id = ? AND is_active = 1",
                    conn, params=[task_id]
                )
                conn.close()
                return df

            query = "SELECT * FROM tasks WHERE is_active = 1"
            params = []

            if division and division != "All":
                query += " AND division LIKE ?"
                params.append("%{}%".format(division))

            if category and category != "All":
                query += " AND category LIKE ?"
                params.append("%{}%".format(category))

            if search_term:
                query += " AND (title LIKE ? OR task_description LIKE ?)"
                params.extend(["%{}%".format(search_term), "%{}%".format(search_term)])

            query += " ORDER BY title"

            df = pd.read_sql_query(query, conn, params=params)
            return df
        finally:
            conn.close()
    return pd.DataFrame()

# Ensure parent window listens for navigation requests from iframes (install once)
st.markdown("""
<script>
(function(){
  if (window.__va_parent_msg_listener_installed) return;
  window.__va_parent_msg_listener_installed = true;
  window.addEventListener('message', function(e){
    try {
      if (e.data && e.data.va_title_navigate) {
        const params = new URLSearchParams(window.location.search || "");
        params.set('page','notice');
        // set search (reloads) to move to notice page
        window.location.search = '?' + params.toString();
      }
      if (e.data && e.data.va_nav) {
        const params = new URLSearchParams(window.location.search || "");
        params.set('page', e.data.va_nav);
        window.location.search = '?' + params.toString();
      }
    } catch (err) {
      console.warn('va parent msg handler error', err);
    }
  }, false);
})();
</script>
""", unsafe_allow_html=True)

# Page navigation logic: prefer query param when present; initialize to "title" only if session state missing.
try:
    qp = st.query_params
except Exception:
    qp = {}
requested_page = qp.get("page", [None])[0] if qp else None
_allowed_pages = {"title", "notice", "welcome", "main", "edit_task"}
if requested_page in _allowed_pages:
    # Always allow query-param driven navigation to override session_state on reloads
    st.session_state.current_page = requested_page
elif "current_page" not in st.session_state:
    st.session_state.current_page = "title"

def show_title_page():
    """Title screen rendered in an iframe so client JS can reliably run and ask the parent to navigate."""
    title_html = textwrap.dedent("""
    <style>
      /* force iframe content to fill without scrollbars */
      html,body { height:100vh; margin:0; padding:0; overflow:hidden; -webkit-font-smoothing:antialiased; }
      .title-page {
        background: linear-gradient(135deg, #111D42 0%, #1e3a8a 100%);
        color: white;
        height:100vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        padding:0;
        box-sizing:border-box;
      }
      .va-logo-large { width:220px; height:220px; background:white; border-radius:50%; margin-bottom:28px; background-size:contain; background-position:center; background-repeat:no-repeat; }
      .version-badge { position: absolute; right:16px; bottom:16px; background:#2e8540; color:white; padding:6px 12px; border-radius:16px; font-weight:700; }
      .title-main { font-size:48px; font-weight:300; margin:0 0 8px 0; }
      .title-subtitle { font-style:italic; opacity:0.95; margin:0; }
      .va-loader { position: fixed; right: 20px; bottom: 20px; display:flex; align-items:center; gap:8px; pointer-events:none; z-index:9999; }
      .va-loader .spinner { width:18px;height:18px;border-radius:50%;border:3px solid rgba(255,255,255,0.35);border-top-color:#fff;animation:va-spin 1s linear infinite; }
      .va-loader .loader-text { color:#fff; font-weight:600; font-size:14px; text-shadow:0 1px 3px rgba(0,0,0,0.3); }
      @keyframes va-spin { to { transform: rotate(360deg); } }
    </style>

    <div class="title-page" role="main" aria-live="polite">
      <div style="position:relative;">
        <div class="va-logo-large" aria-hidden="true" style="background-image: url('data:image/svg+xml;base64,%s'); background-size:contain;"></div>
        <div class="version-badge">v1.4</div>
      </div>
      <h1 class="title-main">VA AI Assistant</h1>
      <p class="title-subtitle">Built for the VA. Powered by AI.</p>

      <div class="va-loader" aria-hidden="true">
        <div class="spinner" aria-hidden="true"></div>
        <div class="loader-text">Loading...</div>
      </div>
    </div>

    <script>
    // inside iframe -> postMessage to parent after 3s; parent listener will change page
    (function(){
      if (window.__va_title_nav_installed) return;
      window.__va_title_nav_installed = true;
      setTimeout(function(){
        try {
          // prefer postMessage (works when iframe is sandboxed)
          window.parent.postMessage({ va_title_navigate: true }, '*');
        } catch (err) {
          // fallback to direct parent location change when same-origin
          try {
            const p = new URLSearchParams(window.parent.location.search || '');
            p.set('page','notice');
            window.parent.location.search = '?' + p.toString();
          } catch (e) {
            console.warn('title nav fallback failed', e);
          }
        }
      }, 3000);
    })();
    </script>
    """ % (va_seal_b64 or ""))

    # render in iframe so the script executes and can talk to parent
    components_html_with_css(title_html, height=900, scrolling=False)

def show_notice_page():
    """Page 2: Notice screen with proper alignment (iframe button + postMessage -> parent)"""

    # Parent-side listener injected first so it's available when the iframe loads/clicks.
    # Also handle 'va_nav' messages in case other pages want client-side driven navigation.
    st.markdown("""
    <script>
    (function(){
      if (window.__va_ack_listener_installed) return;
      window.__va_ack_listener_installed = true;
      window.addEventListener('message', function(e){
        try {
          if (e.data && e.data.va_ack) {
            const params = new URLSearchParams(window.location.search);
            params.set('ack','1');
            window.location.search = '?' + params.toString();
            return;
          }
          if (e.data && e.data.va_nav) {
            const params = new URLSearchParams(window.location.search);
            params.set('page', e.data.va_nav);
            window.location.search = '?' + params.toString();
          }
        } catch (err) {
          console.warn('ack/nav handling error', err);
        }
      }, false);
    })();
    </script>
    """, unsafe_allow_html=True)

    # iframe HTML includes the acknowledge anchor (.ack-link) exactly where it belongs
    iframe_html = textwrap.dedent("""
    <div class="notice-page">
      <div class="notice-container">
        <div class="notice-header">⚠️ NOTICE ⚠️</div>
        <div class="notice-subtitle">
          Using AI-generated content still<br>requires careful review.
        </div>

        <div class="notice-grid">
          <div class="notice-item">
            <div class="notice-icon">✓</div>
            <div class="notice-content">
              <h4>Verification</h4>
              <p>Ensure the generated information is accurate and relevant</p>
            </div>
          </div>

          <div class="notice-item">
            <div class="notice-icon">✏️</div>
            <div class="notice-content">
              <h4>Customization</h4>
              <p>Adjust content to reflect specific details.</p>
            </div>
          </div>

          <div class="notice-item">
            <div class="notice-icon">🩺</div>
            <div class="notice-content">
              <h4>Clinical judgment</h4>
              <p>Use your expertise to ensure AI-generated recommendations align with current guidelines and practices.</p>
            </div>
          </div>

          <div class="notice-item">
            <div class="notice-icon">🛡️</div>
            <div class="notice-content">
              <h4>Compliance</h4>
              <p>Ensure adherence to documentation standards and legal requirements.</p>
            </div>
          </div>
        </div>

        <div class="notice-acknowledge">
          <a id="ack-anchor" class="ack-link" href="javascript:void(0)">I Acknowledge</a>
        </div>
      </div>
    </div>

    <script>
    (function(){
      const ack = document.getElementById('ack-anchor');
      if (!ack) return;
      ack.addEventListener('click', function(){
        try {
          window.parent.postMessage({va_ack: true}, '*');
        } catch (e) {
          console.warn('postMessage failed', e);
        }
      }, false);
    })();
    </script>
    """)

    # render iframe (keeps styling/layout identical)
    components_html_with_css(iframe_html, height=650, scrolling=False)

    # Python: detect the ack query param (use non-experimental reader st.query_params)
    try:
        params = st.query_params
    except Exception:
        params = {}

    if params.get("ack", ["0"])[0] == "1":
        st.session_state.acknowledged = True
        st.session_state.current_page = "welcome"
        # clear query params so future navigation is clean
        try:
            st.experimental_set_query_params()
        except Exception:
            pass
        st.rerun()

def show_welcome_page():
    """Page 3: Welcome screen with template selection"""

    st.title("Welcome to the VA AI Assistant")

    if "acknowledged" in st.session_state and st.session_state.acknowledged:
        st.markdown(
            "Thank you for acknowledging the notice. You can now use the VA AI Assistant."
        )
    else:
        st.markdown(
            "Please review the notice on the previous page and acknowledge it to proceed."
        )

    # Template selection interface
    st.subheader("Select a template to get started:")
    divisions = load_divisions()
    categories = load_categories()

    # Division and category filters
    col1, col2 = st.columns([2, 3])
    with col1:
        division_filter = st.selectbox(
            "Select Division",
            options=["All"] + divisions["division_name"].tolist(),
            index=0,
            key="division_filter_welcome"
        )
    with col2:
        category_filter = st.selectbox(
            "Select Category",
            options=["All"] + categories["category_name"].tolist(),
            index=0,
            key="category_filter_welcome"
        )

    # Load and display tasks based on filters
    tasks = load_tasks(division=division_filter, category=category_filter)
    if not tasks.empty:
        st.subheader("Available Tasks:")
        for _, task in tasks.iterrows():
            st.markdown(f"- {task['title']}")
    else:
        st.markdown("No tasks found for the selected division and category.")

    # Debug: Show raw tasks data
    if st.checkbox("Show raw tasks data", False):
        st.write(tasks)

def show_main_interface():
    """Main interface for the app after title and notice pages"""

    st.header("VA AI Assistant - Task Management")

    # Division and category filters
    col1, col2 = st.columns([2, 3])
    with col1:
        division_filter = st.selectbox(
            "Select Division",
            options=["All"] + load_divisions()["division_name"].tolist(),
            index=0,
            key="division_filter_main"
        )
    with col2:
        category_filter = st.selectbox(
            "Select Category",
            options=["All"] + load_categories()["category_name"].tolist(),
            index=0,
            key="category_filter_main"
        )

    # Task search and favorite toggle
    search_term = st.text_input("Search tasks")
    show_favorites = st.checkbox("Show favorites only", False, key="show_favorites_main")

    # Load and display tasks based on filters
    tasks = load_tasks(division=division_filter, category=category_filter, search_term=search_term, show_favorites=show_favorites)
    if not tasks.empty:
        st.subheader("Task List")
        for _, task in tasks.iterrows():
            # Task card with expandable details
            with st.expander(task["title"], expanded=False):
                st.markdown(f"**Description:** {task['task_description']}")
                st.markdown(f"**Division:** {task['division']}")
                st.markdown(f"**Category:** {task['category']}")
                st.markdown(f"**Created on:** {task['created_at']}")
                st.markdown(f"**Due date:** {task['due_date']}")
                st.markdown(f"**Status:** {task['status']}")
                st.markdown(f"**Priority:** {task['priority']}")
                st.markdown(f"**Tags:** {task['tags']}")
                st.markdown(f"**AI Suggestions:** {task['ai_suggestions']}")
                st.markdown(f"**References:** {task['references']}")
                st.markdown(f"**Favorites:** {task['is_favorite']}")
    else:
        st.markdown("No tasks found matching the criteria.")

    # Debug: Show raw tasks data
    if st.checkbox("Show raw tasks data", False):
        st.write(tasks)

def show_edit_task_page():
    """Page to edit an existing task"""

    st.header("Edit Task")

    # Load divisions and categories for dropdowns
    divisions = load_divisions()
    categories = load_categories()

    # Task ID is passed via query param; load the task details
    task_id = st.experimental_get_query_params().get("task_id", [None])[0]
    task_details = load_tasks(task_id=task_id) if task_id else pd.DataFrame()

    if task_details.empty:
        st.error("Task not found")
        return

    task = task_details.iloc[0]

    # Task form
    with st.form("edit_task_form"):
        st.text_input("Task ID", value=str(task["task_id"]), disabled=True)
        title = st.text_input("Title", value=task["title"])
        description = st.text_area("Description", value=task["task_description"])
        division = st.selectbox("Division", options=divisions["division_name"].tolist(), index=divisions.index[divisions["division_name"] == task["division"]][0])
        category = st.selectbox("Category", options=categories["category_name"].tolist(), index=categories.index[categories["category_name"] == task["category"]][0])
        due_date = st.date_input("Due date", value=datetime.strptime(task["due_date"], "%Y-%m-%d").date())
        priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"]))
        tags = st.text_input("Tags", value=task["tags"])
        ai_suggestions = st.text_area("AI Suggestions", value=task["ai_suggestions"])
        references = st.text_area("References", value=task["references"])
        is_favorite = st.checkbox("Favorite", value=task["is_favorite"])

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            # Update the task in the database
            conn = get_database_connection()
            if conn:
                try:
                    conn.execute(
                        "UPDATE tasks SET title = ?, task_description = ?, division = ?, category = ?, due_date = ?, priority = ?, tags = ?, ai_suggestions = ?, references = ?, is_favorite = ? WHERE task_id = ?",
                        (title, description, division, category, due_date, priority, tags, ai_suggestions, references, is_favorite, task["task_id"])
                    )
                    conn.commit()
                    st.success("Task updated successfully")
                except Exception as e:
                    st.error(f"Error updating task: {e}")
                finally:
                    conn.close()

# Navigation logic: show the requested page
if st.session_state.current_page == "title":
    show_title_page()
elif st.session_state.current_page == "notice":
    show_notice_page()
elif st.session_state.current_page == "welcome":
    show_welcome_page()
elif st.session_state.current_page == "main":
    show_main_interface()
elif st.session_state.current_page == "edit_task":
    show_edit_task_page()
