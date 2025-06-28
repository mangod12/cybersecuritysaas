"""Simple database creation test."""

import sys
import os
import sqlite3

# Add project to path
sys.path.insert(0, os.getcwd())

print("Creating SQLite database...")

try:
    # Create a simple SQLite database
    db_path = "cybersec_alerts.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a simple test table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert test data
    cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Entry",))
    conn.commit()
    
    # Verify the data
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()
    
    print(f"✅ Database created: {db_path}")
    print(f"📊 Test data: {rows}")
    
    conn.close()
    
    # Check if file exists
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"📁 Database file size: {size} bytes")
    
except Exception as e:
    print(f"❌ Database creation failed: {e}")
    import traceback
    traceback.print_exc()
