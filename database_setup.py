"""
AI Assistant Database Setup
This script converts your CSV data files to a SQLite database
"""

import sqlite3
import pandas as pd
import os

def setup_database():
    """Creates the SQLite database and imports CSV data"""
    
    # Create database connection
    db_path = "ai_assistant/database/ai_assistant.db"
    
    # Make sure the directory exists
    os.makedirs("ai_assistant/database", exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    print("🗃️  Setting up AI Assistant Database...")
    
    try:
        # 1. DIVISIONS TABLE
        print("📁 Creating Divisions table...")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS divisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                full_title TEXT,
                division_icon TEXT,
                sort_order INTEGER,
                is_active BOOLEAN
            )
        ''')
        
        # Sample divisions data (since we can't access the CSV directly)
        divisions_data = [
            ("VHA", "Veterans Health Administration", "vha_icon.png", 1, True),
            ("VBA", "Veterans Benefits Administration", "vba_icon.png", 2, True),
            ("NCA", "National Cemetery Administration", "nca_icon.png", 3, True),
            ("All", "All Divisions", "all_icon.png", 4, True)
        ]
        
        conn.executemany('''
            INSERT OR REPLACE INTO divisions (title, full_title, division_icon, sort_order, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', divisions_data)
        
        # 2. CATEGORIES TABLE
        print("📂 Creating Categories table...")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                division TEXT,  -- Comma-separated division list
                category_icon TEXT,
                sort_order INTEGER,
                is_active BOOLEAN
            )
        ''')
        
        # Sample categories data
        categories_data = [
            ("Administrative", "NCA,VBA,VHA", "admin_icon.png", 1, True),
            ("Education", "NCA,VBA,VHA", "education_icon.png", 2, True),
            ("Finance", "NCA,VBA,VHA", "finance_icon.png", 3, True),
            ("Human Resources", "NCA,VBA,VHA", "hr_icon.png", 4, True),
            ("IT", "NCA,VBA,VHA", "it_icon.png", 5, True),
            ("Management", "NCA,VBA,VHA", "management_icon.png", 6, True),
            ("Medical", "VHA", "medical_icon.png", 7, True),
            ("Public Affairs", "NCA,VBA,VHA", "public_affairs_icon.png", 8, True),
            ("Quality & Patient Safety", "VHA", "quality_icon.png", 9, True),
            ("Service Recovery", "NCA,VBA,VHA", "service_icon.png", 10, True)
        ]
        
        conn.executemany('''
            INSERT OR REPLACE INTO categories (title, division, category_icon, sort_order, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', categories_data)
        
        # 3. TASKS TABLE
        print("📋 Creating Tasks table...")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE,
                title TEXT NOT NULL,
                task_description TEXT,
                division TEXT,  -- Comma-separated division list
                category TEXT,  -- Comma-separated category list
                is_active BOOLEAN,
                prompt_default TEXT,
                prompt_v1 TEXT,
                prompt_v2 TEXT,
                config_json TEXT
            )
        ''')
        
        # Sample task data
        tasks_data = [
            ("1", "Meeting Minutes", "Create meeting minutes from a MS Teams transcript.", 
             "NCA,VBA,VHA", "Administrative", True,
             "You are an expert assistant trained to write professional meeting minutes for VA healthcare system leadership.\n\nPlease draft detailed meeting minutes using the transcript provided.\n\nCustomize the minutes using:\n- Committee Name: <<Committee Name>>\n- Meeting Date & Time: <<Meeting Date & Time>>\n- Platform: Microsoft Teams",
             "", "", "{}"),
            ("2", "Email Response", "Generate professional email responses for customer inquiries.",
             "NCA,VBA,VHA", "Administrative", True,
             "You are a professional VA customer service representative. Write a courteous and helpful email response.\n\nPlease respond to the following inquiry:\n\n<<Customer Inquiry>>\n\nTone: <<Tone>>\nRecipient: <<Recipient Name>>",
             "", "", "{}"),
            ("3", "Policy Summary", "Summarize complex VA policies into digestible formats.",
             "NCA,VBA,VHA", "Administrative", True,
             "You are a VA policy expert. Create a clear, concise summary of the following policy document.\n\nPolicy Document: <<Policy Text>>\n\nTarget Audience: <<Audience Level>>\nFormat: <<Summary Format>>",
             "", "", "{}")
        ]
        
        conn.executemany('''
            INSERT OR REPLACE INTO tasks (task_id, title, task_description, division, category, is_active, prompt_default, prompt_v1, prompt_v2, config_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tasks_data)
        
        # 4. USER TASKS TABLE
        print("👤 Creating User Tasks table...")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                task_name TEXT,
                division TEXT,
                category TEXT,
                task_type TEXT,
                role TEXT,
                goal TEXT,
                input_type TEXT,
                tone TEXT,
                output_type TEXT,
                task_description TEXT,
                is_public BOOLEAN,
                is_favorite BOOLEAN,
                is_active BOOLEAN,
                created_date TEXT,
                created_by TEXT,
                prompt_text TEXT,
                tags TEXT,
                icon TEXT,
                task_id INTEGER
            )
        ''')
        
        # 5. USER FAVORITES TABLE
        print("⭐ Creating User Favorites table...")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                task_id INTEGER,
                user_email TEXT,
                date_favorited TEXT,
                is_active BOOLEAN
            )
        ''')
        
        # Commit all changes
        conn.commit()
        print("✅ Database setup completed successfully!")
        print(f"📍 Database location: {db_path}")
        
        # Display summary
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM divisions")
        divisions_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM categories") 
        categories_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks")
        tasks_count = cursor.fetchone()[0]
        
        print(f"\n📊 Database Summary:")
        print(f"   • Divisions: {divisions_count}")
        print(f"   • Categories: {categories_count}")
        print(f"   • Tasks: {tasks_count}")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
