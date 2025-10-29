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
from urllib.parse import urlencode

# Configure page
_page_icon_path = "ai_assistant/images/VA Seal.png"
_page_icon = _page_icon_path if os.path.exists(_page_icon_path) else "🦅"
st.set_page_config(
    page_title="VA AI Assistant",
    page_icon=_page_icon,
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
        height: 100vh; /* desktop */
        height: 100svh; /* modern viewport units */
        overflow: hidden; /* prevent any page scrollbars */
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
        padding: 0 !important; /* eliminate extra vertical space */
        max-width: none !important;
        height: 100vh;
        height: 100svh;
        overflow: hidden;
        margin: 0 !important;
    }}

    /* Streamlit container adjustments */
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
        overflow: hidden !important;
    }}
    [data-testid="stHeader"] {{ display: none !important; height: 0 !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}

    :root {{
        --va-navy: #111D42;
        --va-blue: #0071bc;
        --va-light-blue: #9bdaf1;
        --va-gold: #FB890D;
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
    /* full-viewport with centered band across the middle */
    .notice-page {{
        height: 100vh;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg,
          transparent 0,
          transparent 35vh,
          var(--va-gray-lightest) 35vh,
          var(--va-gray-lightest) 65vh,
          transparent 65vh,
          transparent 100%);
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
        color: #FB890D; /* high-contrast orange */
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
        color: #ffffff !important;
        padding: 12px 36px;
        border-radius: 12px;
        font-weight: 700;
        text-decoration: none !important;
        box-shadow: 0 8px 20px rgba(17,46,81,0.25);
    }}
    .ack-link:visited, .ack-link:hover, .ack-link:active {{
        color: #ffffff !important;
        text-decoration: none !important;
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
        background: #111D42; /* solid VA Navy per request */
        color: white;
        padding: 4rem 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: 100vh;
        position: relative;
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

    /* ============ HELP PAGES ============ */
    .help-page {{
        min-height: 100vh;
        margin: 0;
        padding: 0 1.5rem 2rem 1.5rem;
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: 1.5rem;
        align-items: start;
        background: var(--va-gray-lightest);
    }}
    .help-sidebar {{
        position: sticky;
        top: 0.75rem;
        align-self: start;
        background: #fff;
        border: 1px solid var(--va-gray-lighter);
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        padding: 1rem;
    }}
    .help-sidebar h4 {{
        margin: 0 0 0.5rem 0;
        color: var(--va-navy);
        font-weight: 800;
    }}
    .help-nav a {{
        display:block;
        padding: 8px 10px;
        margin: 4px 0;
        border-radius: 8px;
        color: var(--va-gray);
        text-decoration: none;
    }}
    .help-nav a:hover {{
        background: var(--va-light-blue);
        color: var(--va-navy);
    }}
    .help-nav a.active {{
        background: var(--va-light-blue);
        color: var(--va-navy);
        font-weight: 700;
    }}
    .help-content {{
        background: #fff;
        border: 1px solid var(--va-gray-lighter);
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }}
    .help-hero {{
        display:flex; align-items:center; justify-content:space-between;
        gap: 1rem; margin-bottom: 1rem;
    }}
    .help-hero .title {{
        color: var(--va-navy); font-size: 1.75rem; font-weight: 800;
    }}
    .help-card {{
        background: var(--va-gray-lightest);
        border: 1px solid var(--va-gray-lighter);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0 1rem 0;
    }}
    .help-step {{ display:flex; align-items:flex-start; gap: 12px; margin: 8px 0; }}
    .help-step .dot {{
        width: 28px; height: 28px; border-radius: 50%;
        background: var(--va-navy); color:#fff; font-weight:800;
        display:flex; align-items:center; justify-content:center;
        box-shadow: 0 4px 10px rgba(17,46,81,0.25);
        flex-shrink:0;
    }}
    .help-step .txt {{ color: var(--va-gray); line-height: 1.5; }}

    /* Help header search */
    .help-search {{
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .help-search input[type="search"] {{
        width: clamp(240px, 40vw, 520px);
        padding: 10px 14px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        outline: none;
    }}

    /* CTA buttons (uniform size for Explore/Help) */
    .cta-btn {{
        display: inline-block;
        padding: 12px 22px;
        border-radius: 12px;
        font-weight: 700;
        min-width: 180px;
        height: 44px;
        text-align: center;
        line-height: 20px;
        text-decoration: none !important;
        cursor: pointer;
        user-select: none;
    }}
    .cta-primary {{
        background: var(--va-navy);
        color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(17,46,81,0.25);
    }}
    .cta-primary:hover {{ filter: brightness(1.05); }}
    .cta-secondary {{
        background: #ffffff;
        color: var(--va-navy) !important;
        border: 1px solid var(--va-gray-lighter);
    }}
    .cta-secondary:hover {{ background: var(--va-light-blue); border-color: var(--va-blue); }}

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

    /* active filter item */
    .division-btn.active, .category-btn.active {{
        background: var(--va-light-blue);
        border-color: var(--va-blue);
        color: var(--va-navy);
        font-weight: 700;
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

# --- Lightweight API handlers (e.g., AJAX favorite toggle) ---
def _toggle_favorite_db(task_id: str):
    if not task_id:
        return
    conn = get_database_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT is_favorite FROM tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            return
        new_val = 0 if int(row[0] or 0) else 1
        cur.execute("UPDATE tasks SET is_favorite = ? WHERE task_id = ?", (new_val, task_id))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def _qp_get_local(qp_obj, key):
    """Small local helper so we don't rely on _get_qp being defined yet."""
    try:
        val = qp_obj.get(key)
        if isinstance(val, (list, tuple)):
            return val[0]
        return val
    except Exception:
        return None

# Handle API calls early and stop rendering to avoid page refresh.
try:
    _qp_api = st.query_params
except Exception:
    _qp_api = {}
_api = _qp_get_local(_qp_api, "api")
if _api == "favt":
    _tid = _qp_get_local(_qp_api, "task")
    if _tid:
        _toggle_favorite_db(_tid)
    st.write("OK")
    st.stop()

def components_html_with_css(inner_html: str, height: int = 600, scrolling: bool = True):
    """
    Render HTML inside Streamlit components with the same css_styles injected
    so the iframe gets the styling. Fail gracefully and show error output.

    Also inject a small override to re-enable scrolling within the iframe.
    The global CSS used by the main app disables scrolling to create a kiosk-like
    layout; inside an iframe this can prevent anchor navigation from working.
    """
    iframe_safe_css = (
        "<style>"
        "html,body{height:auto !important;min-height:0 !important;overflow:auto !important;}"
        ".block-container{height:auto !important;overflow:visible !important;}"
        "</style>"
    )
    full_html = css_styles + "\n" + iframe_safe_css + "\n" + textwrap.dedent(inner_html)
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
def _get_qp(qp_obj, key):
    try:
        val = qp_obj.get(key)
        if isinstance(val, (list, tuple)):
            return val[0]
        if isinstance(val, str):
            return val
        return None
    except Exception:
        return None

try:
    qp = st.query_params
except Exception:
    qp = {}
requested_page = _get_qp(qp, "page") if qp else None
_allowed_pages = {"title", "notice", "welcome", "main", "edit_task", "help", "task"}
if requested_page in _allowed_pages:
    # Always allow query-param driven navigation to override session_state on reloads
    st.session_state.current_page = requested_page
elif "current_page" not in st.session_state:
    st.session_state.current_page = "title"

def show_title_page():
    """Title screen styled like scrWelcome: framed white canvas with left logo and right title/tagline."""
    # Try to load the app logo (PNG with transparent background)
    welcome_logo_b64 = None
    for cand in [
        "ai_assistant/images/VA AI Assistant Logo Transparent background.png",
        "ai_assistant/images/welcome_logo.png",
        "ai_assistant/images/VA Welcome Logo.png",
        "ai_assistant/images/VA_Logo.png",
    ]:
        b = get_image_as_base64(cand)
        if b:
            welcome_logo_b64 = b
            break

    title_html = textwrap.dedent("""
    <style>
      html,body { height:100vh; margin:0; padding:0; overflow:hidden; -webkit-font-smoothing:antialiased; }
      body { background: #0f1e42; }
      /* Fill entire viewport with framed canvas (no surrounding whitespace) */
      .welcome-canvas { width: 100vw; height: 100vh; background:#ffffff; border: 20px solid #111D42; border-radius: 8px; display:flex; align-items:center; justify-content:center; position: fixed; top:0; left:0; margin: 0; box-sizing: border-box; }
      .welcome-row { display:flex; align-items:center; gap: 40px; max-width: 1150px; padding: 0 24px; }
      .welcome-logo { width: 260px; height: 260px; border-radius: 50%; background: transparent; box-shadow: 0 18px 48px rgba(0,0,0,0.25); display:flex; align-items:center; justify-content:center; background-image: url("data:image/png;base64,__WELCOME_LOGO_B64__"); background-size: 130% 130%; background-repeat: no-repeat; background-position: center; }
      .welcome-text { display:flex; flex-direction:column; justify-content:center; }
      .welcome-text .brand-title { font-size: 64px; font-weight: 700; color:#111827; margin: 0 0 6px 0; letter-spacing: 0.5px; }
      .welcome-text .tagline { font-size: 20px; font-style: italic; color:#6b7280; margin: 0 0 10px 0; }
      .welcome-text .underline { width: 360px; height: 4px; background:#9aa8c5; border-radius: 2px; margin: 6px 0 8px 0; box-shadow: 0 1px 0 rgba(0,0,0,0.05); }
      .version-badge-static { display:inline-block; background:#2e8540; color:#fff; padding:4px 0; border-radius:14px; font-weight:700; font-size: 14px; margin-top:6px; width:50px; text-align:center; }
      .va-loader { position: absolute; right: 18px; bottom: 12px; display:flex; align-items:center; gap:8px; }
      .va-loader .spinner { width:12px;height:12px;border-radius:50%;border:3px solid rgba(17,29,66,0.25);border-top-color:#111D42;animation:va-spin 1s linear infinite; }
      .va-loader .loader-text { color:#111D42; font-weight:600; font-size:13px; }
      @keyframes va-spin { to { transform: rotate(360deg); } }
    </style>

    <div class="welcome-canvas" role="main" aria-live="polite">
      <div class="welcome-row">
        <div class="welcome-logo"></div>
        <div class="welcome-text">
          <div class="brand-title">VA AI Assistant</div>
          <div class="tagline">Built for the VA. Powered by AI.</div>
          <div class="underline"></div>
          <span class="version-badge-static">v1.4</span>
        </div>
      </div>
      <div class="va-loader" aria-hidden="true">
        <div class="spinner" aria-hidden="true"></div>
        <div class="loader-text">Loading...</div>
      </div>
    </div>

    <script>
    (function(){
      if (window.__va_title_nav_installed) return;
      window.__va_title_nav_installed = true;
      function goNotice(){
        var url = null;
        try {
          var u = new URL(window.location.href);
          u.searchParams.set('page','notice');
          url = u.toString();
        } catch (e) {
          try {
            var qs = new URLSearchParams(window.location.search||'');
            qs.set('page','notice');
            url = '?' + qs.toString();
          } catch(_) {}
        }
        if (url) {
          try {
            // Try anchor click first (often succeeds under CSP)
            var a = document.createElement('a');
            a.href = url; a.style.display='none'; document.body.appendChild(a); a.click();
          } catch(_){ }
          // Redundant fallbacks
          setTimeout(function(){ try{ window.location.replace(url); }catch(_){} }, 50);
          setTimeout(function(){ try{ window.location.href = url; }catch(_){} }, 150);
          try { history.replaceState({}, '', url); window.location.reload(); } catch(_){ }
        }
        // Also message any listeners on this window and parent
        try { window.postMessage({va_nav:'notice'}, '*'); } catch(_){ }
        try { window.parent.postMessage({va_title_navigate:true, va_nav:'notice'}, '*'); } catch (_){ }
      }
      // Run after paint to ensure Streamlit has mounted
      window.requestAnimationFrame(function(){ setTimeout(goNotice, 4500); });
    })();
    </script>
    """)

    title_html = title_html.replace("__WELCOME_LOGO_B64__", welcome_logo_b64 or "")
    # Render directly in main DOM to avoid iframe sizing and enable navigation
    st.markdown(title_html, unsafe_allow_html=True)

    # Server-side, browser-agnostic auto-advance after a short delay
    if not st.session_state.get("va_title_auto_nav_done"):
        st.session_state["va_title_auto_nav_done"] = True
        try:
            time.sleep(4.5)
        except Exception:
            pass
        st.session_state.current_page = "notice"
        try:
            qp_obj = st.query_params
            try:
                qp_obj["page"] = "notice"
            except Exception:
                # fallback: full update
                st.query_params.update({"page": "notice"})
        except Exception:
            pass
        st.rerun()

def show_notice_page_Pre_Mod():
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
    components_html_with_css(iframe_html, height=600, scrolling=False)

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
            st.query_params.clear()
        except Exception:
            pass
        st.rerun()


def show_notice_page():
    """Notice screen centered vertically with a gray band across the middle (Post-Mod)."""
    notice_html = (
"""
<div class="notice-page">
<div class="notice-container">
<div class="notice-header">
  <span style="vertical-align:middle; display:inline-block; margin-right:8px;">
    <svg width="36" height="30" viewBox="0 0 24 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M12 2 L22 18 H2 Z" fill="#FB890D"/>
      <rect x="11" y="7" width="2" height="6" rx="1" fill="#ffffff"/>
      <circle cx="12" cy="15.5" r="1.2" fill="#ffffff"/>
    </svg>
  </span>
  <span style="color:#FB890D">NOTICE</span>
  <span style="vertical-align:middle; display:inline-block; margin-left:8px;">
    <svg width="36" height="30" viewBox="0 0 24 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M12 2 L22 18 H2 Z" fill="#FB890D"/>
      <rect x="11" y="7" width="2" height="6" rx="1" fill="#ffffff"/>
      <circle cx="12" cy="15.5" r="1.2" fill="#ffffff"/>
    </svg>
  </span>
</div>
<div class="notice-subtitle">Using AI-generated content still<br>requires careful review.</div>
<div class="notice-grid">
  <div class="notice-item">
    <div class="notice-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M20 6L9 17l-5-5" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="notice-content"><h4>Verification</h4><p>Ensure the generated information is accurate and relevant</p></div>
  </div>
  <div class="notice-item">
    <div class="notice-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M3 21l3.5-1 11-11-2.5-2.5-11 11L3 21z" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
        <path d="M14.5 6.5l2.5 2.5" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    <div class="notice-content"><h4>Customization</h4><p>Adjust content to reflect specific details.</p></div>
  </div>
  <div class="notice-item">
    <div class="notice-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M7 4v6a5 5 0 0 0 10 0V4" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
        <path d="M12 15v2a3 3 0 0 0 3 3h1a3 3 0 0 0 3-3" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
        <circle cx="6" cy="18" r="2" stroke="#ffffff" stroke-width="2" fill="none"/>
      </svg>
    </div>
    <div class="notice-content"><h4>Clinical judgment</h4><p>Use your expertise to ensure AI-generated recommendations align with current guidelines and practices.</p></div>
  </div>
  <div class="notice-item">
    <div class="notice-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M12 3l7 4v5c0 5-3.5 7.5-7 9-3.5-1.5-7-4-7-9V7l7-4z" stroke="#ffffff" stroke-width="2" fill="none"/>
        <path d="M9 12l2 2 4-4" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="notice-content"><h4>Compliance</h4><p>Ensure adherence to documentation standards and legal requirements.</p></div>
  </div>
</div>
<div class="notice-acknowledge"><a id="ack-anchor" class="ack-link" href="?page=welcome&ack=1" target="_self" onclick="try{event.preventDefault();var p=new URLSearchParams(window.location.search||'');p.set('page','welcome');p.set('ack','1');window.location.search='?'+p.toString();}catch(e){window.location.href='?page=welcome&ack=1';}">I Acknowledge</a></div>
</div>
</div>
<script>
 (function(){
   // no-op script kept for safety; anchor now navigates directly via href
 })();
</script>
"""
    )

    st.markdown(notice_html, unsafe_allow_html=True)

    try:
        params = st.query_params
    except Exception:
        params = {}

    if (params.get("ack", ["0"])[0] if isinstance(params, dict) else _get_qp(params, "ack")) == "1":
        st.session_state.acknowledged = True
        st.session_state.current_page = "welcome"
        try:
            st.query_params.clear()
        except Exception:
            pass
        st.rerun()

def show_welcome_page():
    """Page 3: Onboarding-style welcome screen (scrOnboarding)."""

    # Count templates if available
    try:
        templates_df = load_tasks()
        tmpl_count = int(templates_df.shape[0]) if not templates_df.empty else 0
    except Exception:
        tmpl_count = 0

    onboarding_html = textwrap.dedent("""
    <div class="welcome-page">
      <div class="welcome-left">
        <div class="va-seal" aria-hidden="true"></div>
        <h1 class="welcome-title">VA AI Assistant</h1>
        <div class="welcome-subtitle">Built for the VA. Powered by AI.</div>
      </div>
      <div class="welcome-right">
        <div class="welcome-content">
          <h2>Let's Get Started</h2>
          <p>Choose how you'd like to explore AI-powered tools designed specifically for VA employees. Our assistant helps you generate professional prompts for common tasks across all VA divisions.</p>
          <div style="display:flex; gap:14px; justify-content:center;">
            <a id="explore-btn" class="ack-link" href="?page=main">Explore Tasks ▶</a>
            <a id="help-btn" class="cta-btn cta-secondary" href="?page=help" target="_self">Help &amp; How It Works</a>
          </div>
          <div class="template-count">⚠ (__TMPL_COUNT__) AI prompt templates available</div>
        </div>
      </div>
    </div>
    <script>
    (function(){
      var ex = document.getElementById('explore-btn');
      if (ex) ex.addEventListener('click', function(e){
        try { e.preventDefault(); } catch(_){ }
        try {
          var p = new URLSearchParams(window.location.search||'');
          p.set('page','main');
          var url='?'+p.toString();
          window.location.replace(url);
        } catch (err) { console.warn('explore nav failed', err); }
      });
      var hb = document.getElementById('help-btn');
      if (hb) hb.addEventListener('click', function(e){
        try { e.preventDefault(); } catch(_){ }
        try {
          var p = new URLSearchParams(window.location.search||'');
          p.set('page','help');
          var url='?'+p.toString();
          window.location.replace(url);
        } catch (err) { console.warn('help nav failed', err); }
      });
    })();
    </script>
    """)

    onboarding_html = onboarding_html.replace("__TMPL_COUNT__", str(tmpl_count))
    # Normalize buttons: make Explore/Help same size and fix symbols
    onboarding_html = (onboarding_html
                       .replace('class="ack-link"', 'class="cta-btn cta-primary"')
                       .replace('class="division-btn"', 'class="cta-btn cta-secondary"')
                       .replace('Explore Tasks ▶', 'Explore Tasks ▶')
                       .replace('__TMPL_COUNT__', '⚠ (__TMPL_COUNT__)')
                      )

    # Ensure final labels are correct
    try:
        onboarding_html = (onboarding_html
                           .replace('Explore Tasks ▶', 'Explore Tasks ▶')
                           
                           .replace('⚠ (__TMPL_COUNT__)', '__TMPL_COUNT__')
                          )
    except Exception:
        pass

    st.markdown(onboarding_html, unsafe_allow_html=True)

    # Clear transient query params like ack so URL remains clean after arrival
    try:
        qp = st.query_params
        if qp:
            try:
                if "ack" in qp:
                    del qp["ack"]
            except Exception:
                pass
    except Exception:
        pass

def show_help_page():
    """Recreated Help & How It Works (modeled after scrHelp)."""
    help_html = """
<div class="main-header">
  <div class="header-logo"><div class="header-logo-icon"></div> <span>Help &amp; How It Works</span></div>
  <div class="help-search"><input id="help-search" type="search" placeholder="Search help..." aria-label="Search help" /></div>
  <div style="width:120px"></div>
</div>

<div class="help-page">
  <aside class="help-sidebar">
    <h4>Guide</h4>
    <nav class="help-nav">
      <a href="#help-start">Getting Started</a>
      <a href="#help-nav">Navigation</a>
      <a href="#help-find">Finding Tasks</a>
      <a href="#help-create">Creating Tasks</a>
      <a href="#help-customize">Customizing Prompts</a>
      <a href="#help-favorites">Using Favorites</a>
      <a href="#help-best">Best Practices</a>
      <a href="#help-trouble">Troubleshooting</a>
    </nav>
    <div style="margin-top:12px; text-align:center;">
      <a class="cta-btn cta-secondary" href="?page=welcome">Back</a>
    </div>
  </aside>
  <section class="help-content" id="help-content">
    <section class="help-section" id="help-start" data-label="Getting Started">
      <div class="help-hero"><div class="title">Getting Started</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">From the Welcome screen, click <b>Explore Tasks</b> to open the main catalog of AI templates.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Use the division and category filters (left) or the search box to quickly focus the list.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Click any task card to view full details, instructions, and its AI prompt.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-nav" data-label="Navigation">
      <div class="help-hero"><div class="title">Navigation</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Top Bar</b>: Use the header to return Home or open Help.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Filters</b>: Division and Category buttons refine the visible tasks.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Search</b>: Type key words (e.g., “summary”, “report”) to find matching templates.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-find" data-label="Finding Tasks">
      <div class="help-hero"><div class="title">Finding Tasks</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Browse by <b>Division</b> (e.g., Clinical, Administrative) to narrow context.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Pick a <b>Category</b> (e.g., Documentation, Communication) for specific workflows.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Use <b>Search</b> for quick discovery across all tasks.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-create" data-label="Creating Tasks">
      <div class="help-hero"><div class="title">Creating Tasks</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Open a template and click <b>Create/Edit</b> to add or refine its content.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Provide a descriptive <b>Title</b>, <b>Description</b>, and assign a Division/Category.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Save the task and it becomes available in the catalog with your settings.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-customize" data-label="Customizing Prompts">
      <div class="help-hero"><div class="title">Customizing Prompts</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt">Start from a curated prompt and tailor <b>patient details</b>, <b>context</b>, and <b>tone</b>.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Use placeholders like <code>[DATE]</code>, <code>[UNIT]</code>, <code>[GOAL]</code> to keep prompts reusable.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Preview output, then iterate to improve clarity or reduce length.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-favorites" data-label="Using Favorites">
      <div class="help-hero"><div class="title">Using Favorites</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Click the <b>★</b> icon on any task to mark it as a favorite.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Filter the catalog by <b>Favorites</b> to see only starred items.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-best" data-label="Best Practices">
      <div class="help-hero"><div class="title">Best Practices</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Verify</b> all AI-assisted content for accuracy and relevance before use.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Customize</b> prompts to reflect site-specific or case-specific details.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Comply</b> with VA policies and documentation standards at all times.</div></div>
      </div>
    </section>

    <section class="help-section" id="help-trouble" data-label="Troubleshooting">
      <div class="help-hero"><div class="title">Troubleshooting</div></div>
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt"><b>No results?</b> Clear filters, broaden your search, or switch divisions.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt"><b>Styling issues?</b> Refresh the browser or clear cache to reload app CSS.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt"><b>Navigation not advancing?</b> Ensure you acknowledged the notice and avoid blocking popups or scripts.</div></div>
      </div>
    </section>

    <div style="text-align:center; margin-top: 16px;">
      <a class="cta-btn cta-secondary" href="?page=welcome">Back to Welcome</a>
    </div>
  </section>
</div>

<script>
(function(){
  const input = document.getElementById('help-search');
  const sections = Array.from(document.querySelectorAll('.help-section'));
  const links = Array.from(document.querySelectorAll('.help-nav a'));

  function setActive(id){
    links.forEach(a => {
      const target = (a.getAttribute('href')||'').replace(/^.*#/, '');
      a.classList.toggle('active', !!id && target === id);
    });
  }

  function showOnly(id){
    sections.forEach(sec => { sec.style.display = (!id || sec.id === id) ? '' : 'none'; });
    setActive(id);
  }

  function applyFromHash(){
    const hash = (location.hash || '').replace('#','');
    const found = sections.some(s => s.id === hash);
    const id = found ? hash : 'help-start';
    showOnly(id);
  }

  function filterHelp(q){
    const term = (q||'').trim().toLowerCase();
    if (term){
      sections.forEach(sec => {
        const text = sec.textContent.toLowerCase();
        sec.style.display = text.includes(term) ? '' : 'none';
      });
      setActive(null);
    } else {
      applyFromHash();
    }
  }

  links.forEach(a => {
    a.addEventListener('click', function(e){
      e.preventDefault();
      const id = (this.getAttribute('href')||'').replace(/^.*#/, '');
      if (input) input.value = '';
      history.replaceState(null, '', '#' + id);
      showOnly(id);
      const cont = document.getElementById('help-content');
      if (cont){ window.scrollTo({ top: cont.offsetTop - 10, behavior: 'smooth' }); }
    });
  });

  if (input){ input.addEventListener('input', e => filterHelp(e.target.value)); }
  window.addEventListener('hashchange', applyFromHash);
  applyFromHash();

  // Route any links like "?page=welcome" to parent via postMessage
  try {
    Array.from(document.querySelectorAll('a[href^="?page="]')).forEach(a => {
      a.addEventListener('click', function(e){
        e.preventDefault();
        try {
          var href = this.getAttribute('href') || '';
          var page = (href.split('?')[1]||'').split('#')[0].split('&').map(function(kv){return kv.split('=');}).filter(function(kv){return kv[0]==='page';})[0];
          var val = page && page[1] ? decodeURIComponent(page[1]) : null;
          if (val) { window.parent.postMessage({va_nav: val}, '*'); }
        } catch(_){}
      });
    });
  } catch(_){ }
})();
</script>
"""

    # Normalize any stray bell characters and enrich help content
    try:
        help_html = help_html.replace('<div class="dot">\a</div>', '<div class="dot">•</div>')
        # Getting Started: add steps 4-5
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">From the Welcome screen, click <b>Explore Tasks</b> to open the main catalog of AI templates.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Use the division and category filters (left) or the search box to quickly focus the list.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Click any task card to view full details, instructions, and its AI prompt.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">From the Welcome screen, click <b>Explore Tasks</b> to open the main catalog of AI templates.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Use the division and category filters (left) or the search box to quickly focus the list.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Click any task card to view full details, instructions, and its AI prompt.</div></div>
        <div class="help-step"><div class="dot">4</div><div class="txt">Mark frequently used templates with the <b>star</b> icon and filter by <b>Favorites</b>.</div></div>
        <div class="help-step"><div class="dot">5</div><div class="txt">Open <b>Help</b> anytime from the header to learn features or troubleshoot.</div></div>
      </div>
""",
        )

        # Navigation: swap bullets and add pagination + task cards notes
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Top Bar</b>: Use the header to return Home or open Help.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Filters</b>: Division and Category buttons refine the visible tasks.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Search</b>: Type key words (e.g., "summary", "report") to find matching templates.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Top Bar</b>: Use the header to return Home or open Help.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Filters</b>: Division and Category buttons refine the visible tasks.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Search</b>: Type key words (e.g., "summary", "report") to find matching templates.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Pagination</b>: Use <i>Prev</i>/<i>Next</i> and the page indicator to browse more results.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Task Cards</b>: Click a card title to open details; use the star to favorite.</div></div>
      </div>
""",
        )

        # Finding Tasks: add combination/reset tips
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Browse by <b>Division</b> (e.g., Clinical, Administrative) to narrow context.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Pick a <b>Category</b> (e.g., Documentation, Communication) for specific workflows.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Use <b>Search</b> for quick discovery across all tasks.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Browse by <b>Division</b> (e.g., Clinical, Administrative) to narrow context.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Pick a <b>Category</b> (e.g., Documentation, Communication) for specific workflows.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Use <b>Search</b> for quick discovery across all tasks.</div></div>
        <div class="help-step"><div class="dot">4</div><div class="txt">Combine filters + search to pinpoint exactly what you need.</div></div>
        <div class="help-step"><div class="dot">5</div><div class="txt">To reset, set Division to <b>All</b> and clear the search box.</div></div>
      </div>
""",
        )

        # Creating Tasks: expand details fields
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Open a template and click <b>Create/Edit</b> to add or refine its content.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Provide a descriptive <b>Title</b>, <b>Description</b>, and assign a Division/Category.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Save the task and it becomes available in the catalog with your settings.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Open a template and click <b>Create/Edit</b> to add or refine its content.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Provide a descriptive <b>Title</b>, <b>Description</b>, and assign a Division/Category.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Use <b>Due date</b>, <b>Priority</b>, <b>Tags</b>, and <b>References</b> to keep work organized.</div></div>
        <div class="help-step"><div class="dot">4</div><div class="txt">Click <b>Save</b>. Your task appears in the catalog with your selections.</div></div>
      </div>
""",
        )

        # Customizing Prompts: expand bullets and add privacy/examples
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt">Start from a curated prompt and tailor <b>patient details</b>, <b>context</b>, and <b>tone</b>.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Use placeholders like <code>[DATE]</code>, <code>[UNIT]</code>, <code>[GOAL]</code> to keep prompts reusable.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Preview output, then iterate to improve clarity or reduce length.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt">Start from a curated prompt and tailor <b>patient details</b>, <b>context</b>, and <b>tone</b>.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Use placeholders like <code>[DATE]</code>, <code>[UNIT]</code>, <code>[GOAL]</code> to keep prompts reusable.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt">Preview output, then iterate to improve clarity or reduce length.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Privacy</b>: Do not include PHI/PII unless authorized and required.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Examples</b>: Provide short, concrete examples to guide tone and structure.</div></div>
      </div>
""",
        )

        # Using Favorites: add more steps and clarify star
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Click the <b>?</b> icon on any task to mark it as a favorite.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Filter the catalog by <b>Favorites</b> to see only starred items.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt">Click the <b>star</b> icon on any task to mark it as a favorite.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt">Use the <b>Favorites</b> toggle to view only your starred items.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt">Star/unstar from the task card or details page; changes apply instantly.</div></div>
        <div class="help-step"><div class="dot">4</div><div class="txt">Favorites help you build a quick-access list across divisions and categories.</div></div>
      </div>
""",
        )

        # Best Practices: add concise tip
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Verify</b> all AI-assisted content for accuracy and relevance before use.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Customize</b> prompts to reflect site-specific or case-specific details.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Comply</b> with VA policies and documentation standards at all times.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Verify</b> all AI-assisted content for accuracy and relevance before use.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Customize</b> prompts to reflect site-specific or case-specific details.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Comply</b> with VA policies and documentation standards at all times.</div></div>
        <div class="help-step"><div class="dot">•</div><div class="txt"><b>Be concise</b>: Short, clear inputs yield better results than long, multi-topic prompts.</div></div>
      </div>
""",
        )

        # Troubleshooting: add empty catalog note
        help_html = help_html.replace(
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt"><b>No results?</b> Clear filters, broaden your search, or switch divisions.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt"><b>Styling issues?</b> Refresh the browser or clear cache to reload app CSS.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt"><b>Navigation not advancing?</b> Ensure you acknowledged the notice and avoid blocking popups or scripts.</div></div>
      </div>
""",
            """
      <div class="help-card">
        <div class="help-step"><div class="dot">1</div><div class="txt"><b>No results?</b> Clear filters, broaden your search, or switch divisions.</div></div>
        <div class="help-step"><div class="dot">2</div><div class="txt"><b>Styling issues?</b> Refresh the browser or clear cache to reload app CSS.</div></div>
        <div class="help-step"><div class="dot">3</div><div class="txt"><b>Navigation not advancing?</b> Ensure you acknowledged the notice and avoid blocking popups or scripts.</div></div>
        <div class="help-step"><div class="dot">4</div><div class="txt"><b>Empty catalog?</b> If the database is unavailable, sample cards appear—try again later or contact support.</div></div>
      </div>
""",
        )
    except Exception:
        pass

    # Render via components in an iframe with scrolling enabled. Our helper also
    # injects iframe-safe CSS to restore scrolling and prevent overflow issues.
    components_html_with_css(help_html, height=900, scrolling=True)

def show_main_interface():
    """Tasks UI modeled after scrTasks.png; resilient if DB is empty/missing columns."""

    def _safe_list(df, col, default_list):
        try:
            if isinstance(df, pd.DataFrame) and col in df.columns:
                vals = [v for v in df[col].dropna().astype(str).tolist() if v]
                return sorted(list(dict.fromkeys(vals))) or default_list
        except Exception:
            pass
        return default_list

    # Load filters with safe fallbacks
    divisions_df = load_divisions()
    categories_df = load_categories()
    divisions = ["VHA", "VBA", "NCA"]
    categories = [
        "Administrative","Education","Finance","Human Resources","IT",
        "Management","Medical","Public Affairs","Quality & Patient Safety","Service Recovery"
    ]
    divisions = _safe_list(divisions_df, "division_name", divisions)
    categories = _safe_list(categories_df, "category_name", categories)

    # Read query params to allow link-based navigation
    try:
        _qp = st.query_params
    except Exception:
        _qp = {}
    qp_div = _get_qp(_qp, "div") or "All"
    qp_cat = _get_qp(_qp, "cat") or "All"
    qp_q = _get_qp(_qp, "q") or ""
    qp_fav = _get_qp(_qp, "fav") or "0"
    qp_mine = _get_qp(_qp, "mine") or "0"
    try:
        qp_page = int(_get_qp(_qp, "p") or "1")
        if qp_page < 1:
            qp_page = 1;
    except Exception:
        qp_page = 1
    qp_fav_toggle = _get_qp(_qp, "favt")
    qp_task = _get_qp(_qp, "task")

    # Optional: toggle favorite via query param (favt=task_id)
    def _toggle_favorite(task_id: str):
        conn = get_database_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT is_favorite FROM tasks WHERE task_id = ?", (task_id,))
            row = cur.fetchone()
            if row is None:
                return
            new_val = 0 if int(row[0] or 0) else 1
            cur.execute("UPDATE tasks SET is_favorite = ? WHERE task_id = ?", (new_val, task_id))
            conn.commit()
        except Exception:
            pass
        finally:
            conn.close()

    if qp_fav_toggle:
        _toggle_favorite(qp_fav_toggle)
        try:
            # remove favt from URL and rerun to reflect new state
            upd = {
                "page": "main",
                "div": qp_div,
                "cat": qp_cat,
                "q": qp_q,
                "fav": qp_fav,
                "mine": qp_mine,
            }
            st.query_params.update(upd)
        except Exception:
            pass
        st.rerun()

    # Layout: left filter rail (HTML buttons), right content
    rail, main = st.columns([1, 4])
    with rail:
        st.markdown("### Division")
        items = [
            ("All", ""),
            ("VHA", "vha-icon"),
            ("VBA", "vba-icon"),
            ("NCA", "nca-icon"),
        ]
        div_html = []
        for label, icon_cls in items:
            active = " active" if (qp_div == label) else ""
            href = f"?page=main&div={label}&cat={qp_cat}"
            icon = f"<div class='btn-icon {icon_cls}'></div>" if icon_cls else "<div class='btn-icon'></div>"
            div_html.append(f"<a class='division-btn{active}' href='{href}'>{icon}<span>{label}</span></a>")
        st.markdown("\n".join(div_html), unsafe_allow_html=True)

        st.markdown("### Category")
        cat_map = [
            ("All", ""),
            ("Administrative", "administrative-icon"),
            ("Education", "education-icon"),
            ("Finance", "finance-icon"),
            ("Human Resources", "hr-icon"),
            ("IT", "it-icon"),
            ("Management", "management-icon"),
            ("Medical", "medical-icon"),
            ("Public Affairs", ""),
            ("Quality & Patient Safety", "qps-icon"),
            ("Service Recovery", ""),
        ]
        cat_html = []
        for label, icon_cls in cat_map:
            active = " active" if (qp_cat == label) else ""
            href = f"?page=main&div={qp_div}&cat={label}"
            icon = f"<div class='btn-icon {icon_cls}'></div>" if icon_cls else "<div class='btn-icon'></div>"
            cat_html.append(f"<a class='category-btn{active}' href='{href}'>{icon}<span>{label}</span></a>")
        st.markdown("\n".join(cat_html), unsafe_allow_html=True)

    with main:
        top = st.columns([4, 1, 1, 1])
        with top[0]:
            search_term = st.text_input("Search tasks and prompts...", value=qp_q, key="task_search_main")
        with top[1]:
            show_favorites = st.toggle("Favorites", value=(qp_fav == "1"), key="fav_toggle")
        with top[2]:
            my_tasks = st.toggle("My Tasks", value=(qp_mine == "1"), key="mine_toggle")
        with top[3]:
            if st.button("+ Create Task"):
                st.session_state.current_page = "edit_task"
                st.rerun()

        # keep URL in sync with current controls
        try:
            st.query_params.update({
                "page": "main",
                "div": qp_div,
                "cat": qp_cat,
                "q": search_term or "",
                "fav": "1" if show_favorites else "0",
                "mine": "1" if my_tasks else "0",
                "p": str(qp_page),
            })
        except Exception:
            pass

        # Fetch tasks safely
        tasks = load_tasks(division=qp_div, category=qp_cat, search_term=search_term, show_favorites=show_favorites)
        # Additional client-side filters (robust to missing columns)
        try:
            if search_term:
                needle = str(search_term).lower()
                def _match_row(r):
                    t = str(r.get('title','')).lower()
                    d = str(r.get('task_description','')).lower()
                    return (needle in t) or (needle in d)
                tasks = tasks[tasks.apply(_match_row, axis=1)] if isinstance(tasks, pd.DataFrame) else tasks
        except Exception:
            pass
        try:
            if show_favorites and isinstance(tasks, pd.DataFrame) and 'is_favorite' in tasks.columns:
                tasks = tasks[tasks['is_favorite'].fillna(0).astype(int) == 1]
        except Exception:
            pass
        try:
            if my_tasks and isinstance(tasks, pd.DataFrame):
                # Filter by 'created_by' or 'owner' if present. If not, keep as-is.
                for owner_col in ('created_by','owner','user'):
                    if owner_col in tasks.columns and 'current_user' in st.session_state:
                        tasks = tasks[tasks[owner_col].astype(str) == str(st.session_state['current_user'])]
                        break
        except Exception:
            pass
        if tasks is None or not isinstance(tasks, pd.DataFrame) or tasks.empty:
            # Provide a few sample cards when DB has no rows
            tasks = pd.DataFrame([
                {"title":"Meeting Minutes","task_description":"Create meeting minutes from a transcript","division":"Administrative","category":"Management","is_favorite":1},
                {"title":"Ambient Dictation","task_description":"Generate outpatient clinic notes from a transcript","division":"Medical","category":"Documentation","is_favorite":0},
                {"title":"Market Pay Review","task_description":"Comprehensive market pay review summary","division":"Human Resources","category":"Compensation","is_favorite":0},
                {"title":"Benefits Claim Status","task_description":"Professional letter updating a veteran","division":"Public Affairs","category":"Communication","is_favorite":0},
            ])

        # Ensure task_id column present for links/toggles
        if "task_id" not in tasks.columns:
            tasks = tasks.copy()
            tasks["task_id"] = [str(i+1) for i in range(len(tasks))]

        # Pagination
        page_size = 9
        total = len(tasks)
        total_pages = max(1, (total + page_size - 1) // page_size)
        if qp_page > total_pages:
            qp_page = total_pages
        start = (qp_page - 1) * page_size
        end = start + page_size
        page_df = tasks.iloc[start:end]

        # Grid of cards (3 per row)
        st.markdown("\n")
        # Install JS helper for instant favorite toggle (no full page reload)
        st.markdown(
            """
            <script>
            window.vaFavToggle = async function(tid, el){
              try{
                el.style.opacity = 0.4;
                await fetch('?api=favt&task=' + encodeURIComponent(tid), {credentials:'same-origin'});
                el.textContent = (el.textContent.trim() === '★') ? '☆' : '★';
              }catch(e){ console.warn('toggle fav failed', e); }
              finally{ el.style.opacity = 1; }
            };
            </script>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(3, gap="large")
        base_params = {
            "page": "main",
            "div": qp_div,
            "cat": qp_cat,
            "q": search_term or "",
            "fav": "1" if show_favorites else "0",
            "mine": "1" if my_tasks else "0",
            "p": str(qp_page),
        }
        for i, (_, task) in enumerate(page_df.iterrows()):
            c = cols[i % 3]
            with c:
                tid = str(task.get("task_id", ""))
                # normalize star glyphs for favorite toggle
                fav_star = '★' if int(task.get('is_favorite',0)) else '☆'
                fav_href = "?" + urlencode(dict(base_params, favt=tid))
                details_href = "?" + urlencode(dict(base_params, page="task", task=tid))
                html = f"""
                <div class='task-card'>
                  <div class='task-header'>
                    <h4 class='task-title'><a href='{details_href}' target='_self' style='text-decoration:none;color:inherit;'>{task.get('title','Untitled')}</a></h4>
                    <div class='task-favorite'>
                      <a href='{fav_href}' onclick="event.preventDefault(); window.vaFavToggle('{tid}', this);" title='Toggle favorite' style='text-decoration:none;color:inherit;'>{fav_star}</a>
                    </div>
                  </div>
                  <div class='task-description'>{task.get('task_description','')}</div>
                  <div class='task-footer'>
                    <span class='task-category'>{task.get('category','')}</span>
                    <span class='task-arrow'><a href='{details_href}' target='_self' style='text-decoration:none;color:inherit;'>›</a></span>
                  </div>
                </div>
                """
                # Polish: nicer chevron for task link
                try:
                    html = html.replace("color:inherit;'>></a>", "color:inherit;'>›</a>")
                except Exception:
                    pass
                st.markdown(html, unsafe_allow_html=True)

        # Pagination controls
        nav_cols = st.columns([1,2,1])
        with nav_cols[0]:
            if qp_page > 1 and st.button('◀ Prev', use_container_width=True):
                try:
                    st.query_params.update(dict(base_params, p=str(qp_page-1)))
                except Exception:
                    pass
                st.rerun()
        with nav_cols[1]:
            st.write(f"Page {qp_page} of {total_pages}")
        with nav_cols[2]:
            if qp_page < total_pages and st.button('Next ▶', use_container_width=True):
                try:
                    st.query_params.update(dict(base_params, p=str(qp_page+1)))
                except Exception:
                    pass
                st.rerun()

        # Optional debug table
        if st.checkbox("Show raw tasks data", False):
            st.write(tasks)

        # Details overlay (modal) if a task is requested
        if qp_task:
            detail_df = load_tasks(task_id=qp_task)
            if detail_df is None or detail_df.empty:
                # try to find from current list
                try:
                    detail_df = tasks[tasks["task_id"].astype(str) == str(qp_task)]
                except Exception:
                    detail_df = pd.DataFrame()
            if not detail_df.empty:
                row = detail_df.iloc[0]
                close_href = "?" + urlencode(base_params)
                modal_html = f"""
                <style>
                  .va-modal-backdrop{{position:fixed;inset:0;background:rgba(0,0,0,0.35);z-index:1000;}}
                  .va-modal{{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:min(680px,90vw);background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.3);z-index:1001;padding:20px;border:1px solid var(--va-gray-lighter);}}
                  .va-modal h3{{margin:0 0 8px 0;color:var(--va-navy);}}
                  .va-modal .meta{{color:var(--va-gray);margin-bottom:10px;}}
                  .va-modal .body{{color:var(--va-gray);line-height:1.5;}}
                  .va-modal .grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;color:var(--va-gray);}}
                  .va-modal .grid div{{border:1px solid var(--va-gray-lighter);border-radius:8px;padding:8px;background:var(--va-gray-lightest)}}
                  .va-modal .actions{{margin-top:16px;display:flex;gap:12px;justify-content:flex-end;}}
                  .va-btn{{padding:10px 16px;border-radius:10px;text-decoration:none;border:1px solid var(--va-gray-lighter);}}
                  .va-btn.primary{{background:var(--va-navy);color:#fff;border:none;}}
                </style>
                <a class='va-modal-backdrop' href='{close_href}'></a>
                <div class='va-modal'>
                  <h3>{row.get('title','Untitled')}</h3>
                  <div class='meta'>{row.get('division','')} • {row.get('category','')}</div>
                  <div class='body'>{row.get('task_description','')}</div>
                  <div class='grid'>
                    <div><b>Priority:</b> {row.get('priority','')}</div>
                    <div><b>Due:</b> {row.get('due_date','')}</div>
                    <div style='grid-column:1 / -1'><b>Tags:</b> {row.get('tags','')}</div>
                  </div>
                  <div class='actions'>
                    <a class='va-btn' href='{close_href}'>Close</a>
                    <a class='va-btn primary' href='?page=edit_task&task_id={row.get('task_id','')}' target='_self'>Edit Task</a>
                  </div>
                </div>
                """
                components_html_with_css(modal_html, height=200, scrolling=False)

def show_task_page():
    """Dedicated task details page with actions (opened from the grid)."""
    try:
        _qp = st.query_params
    except Exception:
        _qp = {}
    qp_task = _get_qp(_qp, "task")
    if not qp_task:
        st.error("No task specified")
        return

    # Build a back link preserving filters
    back_params = {
        "page": "main",
        "div": _get_qp(_qp, "div") or "All",
        "cat": _get_qp(_qp, "cat") or "All",
        "q": _get_qp(_qp, "q") or "",
        "fav": _get_qp(_qp, "fav") or "0",
        "mine": _get_qp(_qp, "mine") or "0",
        "p": _get_qp(_qp, "p") or "1",
    }
    back_href = "?" + urlencode(back_params)

    # Load task
    df = load_tasks(task_id=qp_task)
    if df is None or df.empty:
        st.markdown('<div class="main-header"><div class="header-logo"><div class="header-logo-icon"></div> <span>Task Details</span></div></div>', unsafe_allow_html=True)
        st.info("Task not found; it may not exist in the database.")
        st.markdown(f"<a class='cta-btn cta-secondary' href='{back_href}'>Back to Tasks</a>", unsafe_allow_html=True)
        return
    row = df.iloc[0]

    st.markdown('<div class="main-header"><div class="header-logo"><div class="header-logo-icon"></div> <span>Task Details</span></div></div>', unsafe_allow_html=True)

    # Header/meta
    st.markdown(f"## {row.get('title','Untitled')}")
    st.markdown(f"{row.get('division','')} • {row.get('category','')}")
    st.markdown("---")

    # Body
    st.markdown(f"**Description**\n\n{row.get('task_description','')}")
    colm = st.columns(2)
    with colm[0]:
        st.markdown(f"**Priority:** {row.get('priority','')}")
    with colm[1]:
        st.markdown(f"**Due date:** {row.get('due_date','')}")
    st.markdown(f"**Tags:** {row.get('tags','')}")

    # Actions
    act1, act2, act3 = st.columns([1,1,2])
    with act1:
        with st.form("fav_form"):
            fav_val = int(row.get('is_favorite',0))
            new_val = not bool(fav_val)
            st.form_submit_button("★ Favorite" if not fav_val else "☆ Unfavorite")
            if st.session_state.get('fav_form') is not None:
                pass
        # Update favorite on submit (workaround: use a separate button)
        if st.button("Toggle Favorite"):
            conn = get_database_connection()
            if conn:
                try:
                    conn.execute("UPDATE tasks SET is_favorite = ? WHERE task_id = ?", (1 if not fav_val else 0, row.get('task_id')))
                    conn.commit()
                except Exception:
                    pass
                finally:
                    conn.close()
            st.rerun()
    with act2:
        st.markdown(f"<a class='cta-btn cta-primary' href='?page=edit_task&task_id={row.get('task_id','')}' target='_self'>Edit Task</a>", unsafe_allow_html=True)
    with act3:
        st.markdown(f"<a class='cta-btn cta-secondary' href='{back_href}'>Back to Tasks</a>", unsafe_allow_html=True)

def show_edit_task_page():
    """Page to edit an existing task"""
    st.markdown('<div class="main-header"><div class="header-logo"><div class="header-logo-icon"></div> <span>Edit Task</span></div><div></div><div></div></div>', unsafe_allow_html=True)

    # Load divisions and categories for dropdowns
    divisions = load_divisions()
    categories = load_categories()

    # Task ID is passed via query param; load the task details
    try:
        _qp = st.query_params
        _tid = _get_qp(_qp, "task_id")
    except Exception:
        _tid = None
    task_id = _tid
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
        try:
            div_opts = divisions["division_name"].tolist()
            div_idx = divisions.index[divisions["division_name"] == task.get("division","")][0] if not divisions.empty else 0
        except Exception:
            div_opts, div_idx = ["VHA","VBA","NCA"], 0
        division = st.selectbox("Division", options=div_opts, index=min(div_idx, max(0,len(div_opts)-1)))

        try:
            cat_opts = categories["category_name"].tolist()
            cat_idx = categories.index[categories["category_name"] == task.get("category","")][0] if not categories.empty else 0
        except Exception:
            cat_opts, cat_idx = ["Administrative","Medical","IT"], 0
        category = st.selectbox("Category", options=cat_opts, index=min(cat_idx, max(0,len(cat_opts)-1)))

        try:
            due_val = datetime.strptime(task.get("due_date",""), "%Y-%m-%d").date()
        except Exception:
            due_val = datetime.utcnow().date()
        due_date = st.date_input("Due date", value=due_val)
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
elif st.session_state.current_page == "help":
    show_help_page()
elif st.session_state.current_page == "main":
    show_main_interface()
elif st.session_state.current_page == "task":
    show_task_page()
elif st.session_state.current_page == "edit_task":
    show_edit_task_page()
























