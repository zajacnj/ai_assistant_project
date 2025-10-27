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

# Configure page
st.set_page_config(
    page_title="VA AI Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# Enhanced CSS with refined styling
css_styles = f"""
<style>
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    
    /* Reset defaults */
    .main {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    .block-container {{
        padding: 1rem !important;
        max-width: none !important;
    }}
    
    /* VA Colors */
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
    
    /* ============ TITLE PAGE ============ */
    .title-page {{
        background: linear-gradient(135deg, var(--va-navy) 0%, #1e3a8a 100%);
        color: white;
        text-align: center;
        padding: 5rem 2rem;
        margin: -1rem;
        min-height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }}
    
    .va-logo-large {{
        width: 250px;
        height: 250px;
        background: white;
        border-radius: 50%;
        margin: 0 auto 3rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        position: relative;
        {'background-image: url(data:image/svg+xml;base64,' + va_seal_b64 + ');' if va_seal_b64 else ''}
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
    }}
    
    .title-main {{
        font-size: 4.5rem;
        font-weight: 300;
        margin-bottom: 1rem;
        letter-spacing: 3px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    
    .title-subtitle {{
        font-size: 1.8rem;
        opacity: 0.9;
        font-style: italic;
        font-weight: 300;
    }}
    
    .version-badge {{
        position: absolute;
        bottom: -20px;
        right: -20px;
        background: var(--va-green);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    /* ============ NOTICE PAGE ============ */
    .notice-page {{
        background: var(--va-gray-lightest);
        min-height: 100vh;
        padding: 3rem 0;
        margin: -1rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .notice-container {{
        background: white;
        border-radius: 20px;
        padding: 3rem;
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
        gap: 0;
        margin-bottom: 3rem;
        text-align: left;
    }}
    
    .notice-item {{
        background: var(--va-gray-lightest);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid var(--va-navy);
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }}
    
    .notice-item:nth-child(odd) {{
        margin-right: 1rem;
    }}
    
    .notice-item:nth-child(even) {{
        margin-left: 1rem;
    }}
    
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
        margin-top: 2rem;
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
        {'background-image: url(data:image/svg+xml;base64,' + va_seal_b64 + ');' if va_seal_b64 else ''}
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
        {'background-image: url(data:image/svg+xml;base64,' + va_seal_b64 + ');' if va_seal_b64 else ''}
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
    .vha-icon {{ {'background-image: url(data:image/png;base64,' + vha_icon_b64 + ');' if vha_icon_b64 else ''} }}
    .vba-icon {{ {'background-image: url(data:image/png;base64,' + vba_icon_b64 + ');' if vba_icon_b64 else ''} }}
    .nca-icon {{ {'background-image: url(data:image/png;base64,' + nca_icon_b64 + ');' if nca_icon_b64 else ''} }}
    .administrative-icon {{ {'background-image: url(data:image/png;base64,' + admin_icon_b64 + ');' if admin_icon_b64 else ''} }}
    .education-icon {{ {'background-image: url(data:image/png;base64,' + edu_icon_b64 + ');' if edu_icon_b64 else ''} }}
    .finance-icon {{ {'background-image: url(data:image/png;base64,' + finance_icon_b64 + ');' if finance_icon_b64 else ''} }}
    .hr-icon {{ {'background-image: url(data:image/png;base64,' + hr_icon_b64 + ');' if hr_icon_b64 else ''} }}
    .it-icon {{ {'background-image: url(data:image/png;base64,' + it_icon_b64 + ');' if it_icon_b64 else ''} }}
    .management-icon {{ {'background-image: url(data:image/png;base64,' + mgmt_icon_b64 + ');' if mgmt_icon_b64 else ''} }}
    .medical-icon {{ {'background-image: url(data:image/png;base64,' + medical_icon_b64 + ');' if medical_icon_b64 else ''} }}
    .qps-icon {{ {'background-image: url(data:image/png;base64,' + qps_icon_b64 + ');' if qps_icon_b64 else ''} }}
    
    /* Responsive design */
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
        
        .title-main {{
            font-size: 3.5rem;
        }}
        
        .welcome-title {{
            font-size: 2.5rem;
        }}
        
        .welcome-content h2 {{
            font-size: 2rem;
        }}
    }}
    
    @media (max-width: 768px) {{
        .title-main {{
            font-size: 2.5rem;
        }}
        
        .welcome-title {{
            font-size: 2rem;
        }}
        
        .welcome-content h2 {{
            font-size: 1.8rem;
        }}
        
        .va-seal {{
            width: 250px;
            height: 250px;
        }}
        
        .notice-container {{
            padding: 2rem;
            margin: 0 1rem;
        }}
    }}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

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
                conn, params=[f"%{division}%"]
            )
        else:
            df = pd.read_sql_query("SELECT * FROM categories WHERE is_active = 1 ORDER BY sort_order", conn)
        conn.close()
        return df
    return pd.DataFrame()

def load_tasks(division=None, category=None, search_term="", show_favorites=False, show_user_tasks=False):
    """Load tasks from database with filters"""
    conn = get_database_connection()
    if conn:
        query = "SELECT * FROM tasks WHERE is_active = 1"
        params = []
        
        if division and division != "All":
            query += " AND division LIKE ?"
            params.append(f"%{division}%")
            
        if category:
            query += " AND category LIKE ?"
            params.append(f"%{category}%")
            
        if search_term:
            query += " AND (title LIKE ? OR task_description LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
            
        query += " ORDER BY title"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    return pd.DataFrame()

def show_title_page():
    """Page 1: Title screen with SVG VA seal filling circle"""
    
    # Auto-advance timer (invisible)
    if 'title_start_time' not in st.session_state:
        st.session_state.title_start_time = time.time()
    
    elapsed_time = time.time() - st.session_state.title_start_time
    
    # Auto-advance after 3 seconds
    if elapsed_time >= 3:
        st.session_state.current_page = "notice"
        st.rerun()
    
    # Title screen content
    st.markdown("""
    <div class="title-page">
        <div style="position: relative;">
            <div class="va-logo-large"></div>
            <div class="version-badge">v1.4</div>
        </div>
        <h1 class="title-main">VA AI Assistant</h1>
        <p class="title-subtitle">Built for the VA. Powered by AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden timer refresh
    if elapsed_time < 3:
        time.sleep(0.1)
        st.rerun()

def show_notice_page():
    """Page 2: Notice screen with proper alignment"""
    
    st.markdown("""
    <div class="notice-page">
        <div class="notice-container">
            <div class="notice-header">⚠️ NOTICE ⚠️</div>
            <div class="notice-subtitle">
                Using AI-generated content still<br>
                requires careful review.
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
                <button style="background: #112e51; color: white; border: none; padding: 15px 40px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer;">I Acknowledge</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden Streamlit button for functionality
    if st.button("Hidden Acknowledge", key="acknowledge_btn", type="primary"):
        st.session_state.acknowledged = True
        st.session_state.current_page = "welcome"
        st.rerun()

def show_welcome_page():
    """Page 3: Welcome screen with enlarged SVG seal and centered content"""
    
    st.markdown("""
    <div class="welcome-page">
        <div class="welcome-left">
            <div class="va-seal"></div>
            <h1 class="welcome-title">VA AI Assistant</h1>
            <p class="welcome-subtitle">Built for the VA. Powered by AI.</p>
        </div>
        
        <div class="welcome-right">
            <div>
                <h2>Let's Get Started</h2>
                <p>Choose how you'd like to explore AI-powered tools designed specifically for VA employees. Our assistant helps you generate professional prompts for common tasks across all VA divisions.</p>
                
                <div style="display: flex; flex-direction: column; gap: 20px; margin-bottom: 30px;">
                    <button style="background: #112e51; color: white; border: none; padding: 18px 40px; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; transition: all 0.3s ease;" 
                            onmouseover="this.style.background='#1e3a8a'; this.style.transform='translateY(-2px)'" 
                            onmouseout="this.style.background='#112e51'; this.style.transform='translateY(0)'">
                        Explore Tasks ▷
                    </button>
                    <button style="background: transparent; color: #5b616b; border: 2px solid #d6d7d9; padding: 15px 40px; border-radius: 12px; font-size: 16px; cursor: pointer; transition: all 0.3s ease;"
                            onmouseover="this.style.borderColor='#112e51'; this.style.color='#112e51'" 
                            onmouseout="this.style.borderColor='#d6d7d9'; this.style.color='#5b616b'">
                        Help & How It Works
                    </button>
                </div>
                
                <p class="template-count">(34) AI prompt templates available</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden Streamlit buttons for functionality
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hidden Explore", key="explore_btn", type="primary"):
            st.session_state.current_page = "main"
            st.rerun()
    
    with col2:
        if st.button("Hidden Help", key="help_btn"):
            st.info("Help documentation coming soon!")

def show_main_interface():
    """Page 4: Main interface with task management"""
    
    # Initialize session state
    if 'selected_division' not in st.session_state:
        st.session_state.selected_division = ""
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = ""
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    if 'show_favorites' not in st.session_state:
        st.session_state.show_favorites = False
    if 'show_user_tasks' not in st.session_state:
        st.session_state.show_user_tasks = False
    
    # Header with VA branding
    st.markdown("""
    <div class="main-header">
        <div class="header-logo">
            <div class="header-logo-icon"></div>
            VA AI Assistant
        </div>
        <div style="display: flex; gap: 15px;">
            <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">🏠 Home</button>
            <button style="background: #2e8540; border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">+ Create Task</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls bar
    search_col, fav_col, task_col = st.columns([3, 1, 1])
    
    with search_col:
        search_term = st.text_input("", placeholder="Search tasks and prompts...", key="search_input", label_visibility="hidden")
        if search_term != st.session_state.search_term:
            st.session_state.search_term = search_term
    
    with fav_col:
        show_favorites = st.toggle("Favorites (6)", key="favorites_toggle")
        if show_favorites != st.session_state.show_favorites:
            st.session_state.show_favorites = show_favorites
    
    with task_col:
        show_user_tasks = st.toggle("My Tasks (2)", key="user_tasks_toggle")
        if show_user_tasks != st.session_state.show_user_tasks:
            st.session_state.show_user_tasks = show_user_tasks
    
    # Main layout with sidebar
    sidebar_col, content_col = st.columns([1, 3])
    
    with sidebar_col:
        st.markdown("### Division")
        
        divisions_data = [
            {"title": "VHA", "full_title": "Veterans Health Administration", "css_class": "vha-icon"},
            {"title": "VBA", "full_title": "Veterans Benefits Administration", "css_class": "vba-icon"},
            {"title": "NCA", "full_title": "National Cemetery Administration", "css_class": "nca-icon"}
        ]
        
        for division in divisions_data:
            # Create visual button with image
            st.markdown(f"""
            <div class="division-btn">
                <div class="btn-icon {division['css_class']}"></div>
                <span>{division['title']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden functional button
            if st.button(f"Select {division['title']}", 
                        key=f"div_{division['title']}", 
                        help=division['full_title']):
                st.session_state.selected_division = division['title']
                st.session_state.selected_category = ""
                st.rerun()
        
        st.markdown("### Category")
        
        categories_data = [
            {"title": "Administrative", "css_class": "administrative-icon"},
            {"title": "Education", "css_class": "education-icon"},
            {"title": "Finance", "css_class": "finance-icon"},
            {"title": "Human Resources", "css_class": "hr-icon"},
            {"title": "IT", "css_class": "it-icon"},
            {"title": "Medical", "css_class": "medical-icon"},
            {"title": "Management", "css_class": "management-icon"},
            {"title": "Quality & Patient Safety", "css_class": "qps-icon"}
        ]
        
        for category in categories_data:
            # Create visual button with image
            st.markdown(f"""
            <div class="category-btn">
                <div class="btn-icon {category['css_class']}"></div>
                <span>{category['title']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden functional button
            if st.button(f"Select {category['title']}", 
                        key=f"cat_{category['title']}"):
                st.session_state.selected_category = category['title']
                st.rerun()
    
    with content_col:
        st.markdown("## Available Tasks")
        
        # Load and display tasks
        tasks_df = load_tasks(
            division=st.session_state.selected_division,
            category=st.session_state.selected_category,
            search_term=st.session_state.search_term,
            show_favorites=st.session_state.show_favorites,
            show_user_tasks=st.session_state.show_user_tasks
        )
        
        if not tasks_df.empty:
            # Display tasks in enhanced cards
            task_cols = st.columns(2)
            
            for idx, (_, task) in enumerate(tasks_df.iterrows()):
                col_idx = idx % 2
                
                with task_cols[col_idx]:
                    is_favorite = idx % 4 == 0  # Mock favorite status
                    star_icon = "⭐" if is_favorite else "☆"
                    star_color = "#fdb81e" if is_favorite else "#d6d7d9"
                    
                    st.markdown(f"""
                    <div class="task-card">
                        <div class="task-header">
                            <h4 class="task-title">{task['title']}</h4>
                            <span class="task-favorite" style="color: {star_color};">{star_icon}</span>
                        </div>
                        <p class="task-description">{task['task_description']}</p>
                        <div class="task-footer">
                            <span class="task-category">{task.get('category', 'General')}</span>
                            <span class="task-arrow">▶</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Use Task", key=f"use_task_{task['id']}", use_container_width=True):
                        st.session_state.selected_task = task.to_dict()
                        st.success(f"Selected: {task['title']}")
                        st.info("Task customization interface will appear here in the full version.")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 4rem; color: #5b616b;">
                <h3>No tasks found</h3>
                <p style="font-size: 1.1rem;">Try adjusting your search or filter settings.</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application controller"""
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "title"
    if 'acknowledged' not in st.session_state:
        st.session_state.acknowledged = False
    
    # Page routing
    current_page = st.session_state.current_page
    
    if current_page == "title":
        show_title_page()
    elif current_page == "notice":
        show_notice_page()
    elif current_page == "welcome":
        show_welcome_page()
    elif current_page == "main":
        show_main_interface()
    else:
        show_title_page()

if __name__ == "__main__":
    main()
