"""
AI Assistant Application - Main Entry Point
This is your main application file using Streamlit for the web interface.

To run this app:
1. Open Command Prompt/Terminal
2. Navigate to your project folder
3. Type: streamlit run main.py
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="VA AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make it look more professional
st.markdown("""
<style>
    .main-header {
        background-color: #003f7f;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .division-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #003f7f;
        margin-bottom: 1rem;
    }
    
    .task-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    
    .category-badge {
        background-color: #e7f3ff;
        color: #003f7f;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

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
    """Load categories from database, optionally filtered by division"""
    conn = get_database_connection()
    if conn:
        if division and division != "All":
            # Filter categories that include this division
            df = pd.read_sql_query(
                "SELECT * FROM categories WHERE is_active = 1 AND division LIKE ? ORDER BY sort_order", 
                conn, params=[f"%{division}%"]
            )
        else:
            df = pd.read_sql_query("SELECT * FROM categories WHERE is_active = 1 ORDER BY sort_order", conn)
        conn.close()
        return df
    return pd.DataFrame()

def load_tasks(division=None, category=None):
    """Load tasks from database with optional filters"""
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
            
        query += " ORDER BY title"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    return pd.DataFrame()

def show_welcome_screen():
    """Display the welcome/onboarding screen"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 VA AI Assistant</h1>
        <p>Your intelligent companion for Veterans Affairs tasks</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to the AI Assistant!
        
        This application helps VA employees with various AI-powered tasks including:
        
        🏥 **Medical Documentation** - Generate clinical notes and summaries  
        📋 **Administrative Tasks** - Create meeting minutes, emails, and reports  
        💰 **Finance & Claims** - Process benefit calculations and claim reviews  
        👥 **Human Resources** - Draft job descriptions and employee communications  
        🛠️ **IT Support** - Generate technical documentation and procedures  
        
        ### How to Get Started:
        1. **Select a Division** - Choose your VA division (VHA, VBA, NCA)
        2. **Pick a Category** - Browse tasks by category
        3. **Choose a Task** - Select the AI task you need
        4. **Customize & Run** - Personalize the prompt and get results
        """)
        
        if st.button("🚀 Get Started", type="primary", use_container_width=True):
            st.session_state.current_screen = "divisions"
            st.rerun()
    
    with col2:
        st.info("""
        **💡 Tips for Success:**
        
        • Be specific in your requests
        • Provide context when possible  
        • Review AI outputs carefully
        • Save your favorite tasks
        """)
        
        st.warning("""
        **⚠️ Important Notice:**
        
        This is an AI tool to assist with work tasks. Always review and verify AI-generated content before use.
        """)

def show_divisions_screen():
    """Display the divisions selection screen"""
    st.markdown("""
    <div class="main-header">
        <h2>Select Your VA Division</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Welcome"):
        st.session_state.current_screen = "welcome"
        st.rerun()
    
    st.markdown("### Choose the division that best matches your work area:")
    
    divisions_df = load_divisions()
    
    if not divisions_df.empty:
        cols = st.columns(2)
        
        for idx, division in divisions_df.iterrows():
            col = cols[idx % 2]
            
            with col:
                with st.container():
                    st.markdown(f"""
                    <div class="division-card">
                        <h4>{division['title']}</h4>
                        <p>{division['full_title']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Select {division['title']}", key=f"div_{division['id']}", use_container_width=True):
                        st.session_state.selected_division = division['title']
                        st.session_state.current_screen = "categories"
                        st.rerun()

def show_categories_screen():
    """Display the categories screen"""
    division = st.session_state.get('selected_division', 'All')
    
    st.markdown(f"""
    <div class="main-header">
        <h2>Categories - {division}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Divisions"):
            st.session_state.current_screen = "divisions"
            st.rerun()
    
    with col2:
        if st.button("View All Tasks →"):
            st.session_state.selected_category = None
            st.session_state.current_screen = "tasks"
            st.rerun()
    
    st.markdown(f"### Select a category for {division} tasks:")
    
    categories_df = load_categories(division)
    
    if not categories_df.empty:
        cols = st.columns(3)
        
        for idx, category in categories_df.iterrows():
            col = cols[idx % 3]
            
            with col:
                with st.container():
                    # Count tasks in this category
                    tasks_count = len(load_tasks(division, category['title']))
                    
                    st.markdown(f"""
                    <div class="division-card">
                        <h5>{category['title']}</h5>
                        <p>{tasks_count} available tasks</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Select", key=f"cat_{category['id']}", use_container_width=True):
                        st.session_state.selected_category = category['title']
                        st.session_state.current_screen = "tasks"
                        st.rerun()

def show_tasks_screen():
    """Display the tasks screen"""
    division = st.session_state.get('selected_division', 'All')
    category = st.session_state.get('selected_category', None)
    
    st.markdown(f"""
    <div class="main-header">
        <h2>AI Tasks - {division}</h2>
        {f'<p>Category: {category}</p>' if category else '<p>All Categories</p>'}
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Categories"):
            st.session_state.current_screen = "categories"
            st.rerun()
    
    with col2:
        if st.button("🔍 Search Tasks"):
            st.session_state.show_search = not st.session_state.get('show_search', False)
    
    with col3:
        if st.button("➕ Create Custom Task"):
            st.session_state.current_screen = "create_task"
            st.rerun()
    
    # Search functionality
    if st.session_state.get('show_search', False):
        search_term = st.text_input("🔍 Search tasks...", placeholder="Enter keywords to search tasks")
    else:
        search_term = ""
    
    # Load and display tasks
    tasks_df = load_tasks(division, category)
    
    if not tasks_df.empty:
        # Filter by search term if provided
        if search_term:
            mask = tasks_df['title'].str.contains(search_term, case=False, na=False) | \
                   tasks_df['task_description'].str.contains(search_term, case=False, na=False)
            tasks_df = tasks_df[mask]
        
        st.markdown(f"### Found {len(tasks_df)} tasks:")
        
        for idx, task in tasks_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="task-card">
                    <h4>{task['title']}</h4>
                    <p>{task['task_description']}</p>
                    <span class="category-badge">{task['category']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("🚀 Use Task", key=f"use_{task['id']}"):
                        st.session_state.selected_task = task.to_dict()
                        st.session_state.current_screen = "customize_task"
                        st.rerun()
                
                with col2:
                    if st.button("👁️ Preview", key=f"preview_{task['id']}"):
                        with st.expander("Task Preview", expanded=True):
                            st.text_area("Default Prompt:", value=task['prompt_default'], height=150, disabled=True)
                
                with col3:
                    if st.button("⭐ Favorite", key=f"fav_{task['id']}"):
                        st.success("Added to favorites!")
                
                st.divider()
    else:
        st.warning("No tasks found for the selected filters.")

def show_customize_task_screen():
    """Display the task customization screen"""
    task = st.session_state.get('selected_task', {})
    
    if not task:
        st.error("No task selected. Please go back and select a task.")
        if st.button("← Back to Tasks"):
            st.session_state.current_screen = "tasks"
            st.rerun()
        return
    
    st.markdown(f"""
    <div class="main-header">
        <h2>Customize Task: {task['title']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Tasks"):
        st.session_state.current_screen = "tasks"
        st.rerun()
    
    # Task information
    st.markdown(f"**Description:** {task['task_description']}")
    
    # Customization form
    st.markdown("### Customize Your Task:")
    
    with st.form("customize_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            context = st.text_area("Additional Context:", placeholder="Provide any specific context or requirements...")
            audience = st.selectbox("Target Audience:", 
                                  ["General", "Executive Leadership", "Clinical Staff", "Administrative Staff", "Veterans/Families"])
            tone = st.selectbox("Tone:", 
                               ["Professional", "Friendly", "Formal", "Casual", "Empathetic"])
        
        with col2:
            output_format = st.selectbox("Output Format:", 
                                       ["Standard Text", "Bullet Points", "Numbered List", "Table", "Email Format"])
            length = st.selectbox("Length:", 
                                ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (6+ paragraphs)"])
            
            include_examples = st.checkbox("Include Examples")
            include_references = st.checkbox("Include References/Sources")
        
        # Main input area
        st.markdown("### Your Input:")
        main_input = st.text_area("Paste your content here:", 
                                placeholder="Paste the document, transcript, or text you want to process...", 
                                height=200)
        
        # Preview the customized prompt
        st.markdown("### Preview Customized Prompt:")
        
        # Build the customized prompt
        customized_prompt = task['prompt_default']
        
        # Replace placeholders (this is a simplified version)
        if "<<Context>>" in customized_prompt and context:
            customized_prompt = customized_prompt.replace("<<Context>>", context)
        if "<<Audience>>" in customized_prompt and audience:
            customized_prompt = customized_prompt.replace("<<Audience>>", audience)
        if "<<Tone>>" in customized_prompt and tone:
            customized_prompt = customized_prompt.replace("<<Tone>>", tone)
        
        st.text_area("Final Prompt:", value=customized_prompt, height=200, disabled=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate AI Response", type="primary", use_container_width=True)
        
        if submitted:
            if main_input:
                # Here you would integrate with your AI service (ChatGPT, Claude, etc.)
                st.success("✅ Task completed! (In a real implementation, this would call your AI service)")
                
                # Show a sample response
                st.markdown("### AI Generated Response:")
                st.markdown("""
                **Sample AI Response:**
                
                Thank you for using the VA AI Assistant. Your request has been processed successfully.
                
                *Note: This is a sample response. In the full implementation, this would contain the actual AI-generated content based on your customized prompt and input.*
                """)
                
                # Option to save or copy results
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Results"):
                        st.success("Results saved to your workspace!")
                with col2:
                    if st.button("📋 Copy to Clipboard"):
                        st.success("Results copied to clipboard!")
            else:
                st.error("Please provide input content to process.")

def main():
    """Main application function"""
    
    # Initialize session state
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = "welcome"
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🤖 VA AI Assistant")
        st.markdown("---")
        
        # Quick navigation
        st.markdown("### Quick Navigation:")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_screen = "welcome"
            st.rerun()
        
        if st.button("📁 Divisions", use_container_width=True):
            st.session_state.current_screen = "divisions"
            st.rerun()
        
        if st.button("📋 All Tasks", use_container_width=True):
            st.session_state.current_screen = "tasks"
            st.session_state.selected_division = "All"
            st.session_state.selected_category = None
            st.rerun()
        
        if st.button("➕ Create Task", use_container_width=True):
            st.session_state.current_screen = "create_task"
            st.rerun()
        
        st.markdown("---")
        
        # Current selections
        if 'selected_division' in st.session_state:
            st.markdown(f"**Division:** {st.session_state.selected_division}")
        
        if 'selected_category' in st.session_state and st.session_state.selected_category:
            st.markdown(f"**Category:** {st.session_state.selected_category}")
    
    # Main content area
    current_screen = st.session_state.current_screen
    
    if current_screen == "welcome":
        show_welcome_screen()
    elif current_screen == "divisions":
        show_divisions_screen()
    elif current_screen == "categories":
        show_categories_screen()
    elif current_screen == "tasks":
        show_tasks_screen()
    elif current_screen == "customize_task":
        show_customize_task_screen()
    else:
        st.error(f"Unknown screen: {current_screen}")

if __name__ == "__main__":
    main()
