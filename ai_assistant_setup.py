"""
AI Assistant Application - Setup Script
This script creates the basic folder structure for your Python app.
"""

import os

def create_project_structure():
    """Creates the folder structure for the AI Assistant app"""
    
    # Main folders to create
    folders = [
        "ai_assistant",              # Main app folder
        "ai_assistant/database",     # Database files
        "ai_assistant/pages",        # Different screens/pages
        "ai_assistant/components",   # Reusable UI components
        "ai_assistant/models",       # Data models
        "ai_assistant/utils",        # Utility functions
        "ai_assistant/static",       # Static files (CSS, images)
        "ai_assistant/data"          # Sample data files
    ]
    
    # Create each folder
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✅ Created folder: {folder}")
        except Exception as e:
            print(f"❌ Error creating {folder}: {e}")
    
    print("\n🎉 Project structure created successfully!")
    print("Next: Run the database setup script")

if __name__ == "__main__":
    create_project_structure()
