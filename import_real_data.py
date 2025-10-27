"""
CSV Data Import Utility
This script helps you import your actual CSV data from SharePoint exports
into your Python application database.

Instructions:
1. Export your SharePoint lists to CSV files
2. Place them in the ai_assistant/data/ folder
3. Run this script: python import_real_data.py
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

def clean_column_names(df):
    """Clean column names to match our database schema"""
    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    return df

def import_divisions_data():
    """Import divisions data from CSV"""
    print("📁 Importing Divisions data...")
    
    csv_path = "ai_assistant/data/AI_Assistant_Divisions.csv"
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        print("   Please make sure you've exported and placed your Divisions CSV file in ai_assistant/data/")
        return False
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        df = clean_column_names(df)
        
        # Map to our database schema
        df_mapped = pd.DataFrame({
            'title': df.get('title', ''),
            'full_title': df.get('fulltitle', ''),
            'division_icon': df.get('divisionicon', ''),
            'sort_order': pd.to_numeric(df.get('sortorder', 0), errors='coerce').fillna(0),
            'is_active': df.get('isactive', 'True').str.lower() == 'true'
        })
        
        # Connect to database and insert
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        df_mapped.to_sql('divisions', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✅ Imported {len(df_mapped)} divisions")
        return True
        
    except Exception as e:
        print(f"❌ Error importing divisions: {e}")
        return False

def import_categories_data():
    """Import categories data from CSV"""
    print("📂 Importing Categories data...")
    
    csv_path = "ai_assistant/data/AI_Assistant_Categories.csv"
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        df = clean_column_names(df)
        
        df_mapped = pd.DataFrame({
            'title': df.get('title', ''),
            'division': df.get('division', ''),
            'category_icon': df.get('categoryicon', ''),
            'sort_order': pd.to_numeric(df.get('sortorder', 0), errors='coerce').fillna(0),
            'is_active': df.get('isactive', 'True').str.lower() == 'true'
        })
        
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        df_mapped.to_sql('categories', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✅ Imported {len(df_mapped)} categories")
        return True
        
    except Exception as e:
        print(f"❌ Error importing categories: {e}")
        return False

def import_tasks_data():
    """Import tasks data from CSV"""
    print("📋 Importing Tasks data...")
    
    csv_path = "ai_assistant/data/AI_Assistant_Tasks.csv"
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        df = clean_column_names(df)
        
        df_mapped = pd.DataFrame({
            'task_id': df.get('taskid', ''),
            'title': df.get('title', ''),
            'task_description': df.get('task_description', ''),
            'division': df.get('division', ''),
            'category': df.get('category', ''),
            'is_active': df.get('isactive', 'True').str.lower() == 'true',
            'prompt_default': df.get('prompt_default', ''),
            'prompt_v1': df.get('prompt_v1', ''),
            'prompt_v2': df.get('prompt_v2', ''),
            'config_json': df.get('configjson', '{}')
        })
        
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        df_mapped.to_sql('tasks', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✅ Imported {len(df_mapped)} tasks")
        return True
        
    except Exception as e:
        print(f"❌ Error importing tasks: {e}")
        return False

def import_user_tasks_data():
    """Import user tasks data from CSV"""
    print("👤 Importing User Tasks data...")
    
    csv_path = "ai_assistant/data/AI_Assistant_UserTasks.csv"
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        df = clean_column_names(df)
        
        df_mapped = pd.DataFrame({
            'title': df.get('title', ''),
            'task_name': df.get('taskname', ''),
            'division': df.get('division', ''),
            'category': df.get('category', ''),
            'task_type': df.get('tasktype', ''),
            'role': df.get('role', ''),
            'goal': df.get('goal', ''),
            'input_type': df.get('inputtype', ''),
            'tone': df.get('tone', ''),
            'output_type': df.get('outputtype', ''),
            'task_description': df.get('task_description', ''),
            'is_public': df.get('ispublic', 'False').str.lower() == 'true',
            'is_favorite': df.get('isfavorite', 'False').str.lower() == 'true',
            'is_active': df.get('isactive', 'True').str.lower() == 'true',
            'created_date': df.get('createddate', ''),
            'created_by': df.get('createdby', ''),
            'prompt_text': df.get('prompttext', ''),
            'tags': df.get('tags', ''),
            'icon': df.get('icon', ''),
            'task_id': pd.to_numeric(df.get('taskid', 0), errors='coerce').fillna(0)
        })
        
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        df_mapped.to_sql('user_tasks', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✅ Imported {len(df_mapped)} user tasks")
        return True
        
    except Exception as e:
        print(f"❌ Error importing user tasks: {e}")
        return False

def import_favorites_data():
    """Import user favorites data from CSV"""
    print("⭐ Importing User Favorites data...")
    
    csv_path = "ai_assistant/data/AI_Assistant_UserFavorites.csv"
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        df = clean_column_names(df)
        
        df_mapped = pd.DataFrame({
            'title': df.get('title', ''),
            'task_id': pd.to_numeric(df.get('taskid', 0), errors='coerce').fillna(0),
            'user_email': df.get('useremail', ''),
            'date_favorited': df.get('datefavorited', ''),
            'is_active': df.get('isactive', 'True').str.lower() == 'true'
        })
        
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        df_mapped.to_sql('user_favorites', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✅ Imported {len(df_mapped)} user favorites")
        return True
        
    except Exception as e:
        print(f"❌ Error importing user favorites: {e}")
        return False

def verify_data_import():
    """Verify that data was imported correctly"""
    print("\n🔍 Verifying imported data...")
    
    try:
        conn = sqlite3.connect('ai_assistant/database/ai_assistant.db')
        
        # Count records in each table
        tables = ['divisions', 'categories', 'tasks', 'user_tasks', 'user_favorites']
        
        for table in tables:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   📊 {table}: {count} records")
        
        conn.close()
        
        print("\n✅ Data verification completed!")
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")

def main():
    """Main import function"""
    print("🚀 AI Assistant Data Import Utility")
    print("=" * 50)
    
    # Check if data directory exists
    if not os.path.exists("ai_assistant/data"):
        print("❌ Data directory not found!")
        print("   Please create the 'ai_assistant/data' folder and place your CSV files there.")
        print("\n📁 Expected files:")
        print("   • AI_Assistant_Divisions.csv")
        print("   • AI_Assistant_Categories.csv") 
        print("   • AI_Assistant_Tasks.csv")
        print("   • AI_Assistant_UserTasks.csv")
        print("   • AI_Assistant_UserFavorites.csv")
        return
    
    # Check if database exists
    if not os.path.exists("ai_assistant/database/ai_assistant.db"):
        print("❌ Database not found!")
        print("   Please run 'python database_setup.py' first to create the database.")
        return
    
    print("📥 Starting data import process...")
    print()
    
    # Import each data type
    success_count = 0
    
    if import_divisions_data():
        success_count += 1
    
    if import_categories_data():
        success_count += 1
    
    if import_tasks_data():
        success_count += 1
    
    if import_user_tasks_data():
        success_count += 1
    
    if import_favorites_data():
        success_count += 1
    
    # Verify the import
    verify_data_import()
    
    print(f"\n🎉 Import completed! {success_count}/5 data sources imported successfully.")
    
    if success_count == 5:
        print("\n✅ All data imported successfully!")
        print("   You can now run your application: streamlit run main.py")
    else:
        print(f"\n⚠️  {5 - success_count} data sources had issues.")
        print("   Check the error messages above and ensure your CSV files are properly formatted.")

if __name__ == "__main__":
    main()
