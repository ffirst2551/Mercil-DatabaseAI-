"""
Database Initialization Script
สร้างและเตรียม database พร้อมใช้งาน
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()


def init_database():
    """สร้าง database และ extensions"""
    
    # Parse DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    
    # Connect to default postgres database
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Create database if not exists
    db_name = os.getenv('DB_NAME', 'mercil_db')
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"✓ Database '{db_name}' created")
    else:
        print(f"✓ Database '{db_name}' already exists")
    
    cur.close()
    conn.close()
    
    # Connect to the new database
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Create extensions
    extensions = ['postgis', 'vector']
    
    for ext in extensions:
        try:
            cur.execute(f"CREATE EXTENSION IF NOT EXISTS {ext}")
            print(f"✓ Extension '{ext}' enabled")
        except Exception as e:
            print(f"✗ Failed to create extension '{ext}': {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("\n✓ Database initialization completed!")


def create_schema():
    """สร้าง tables และ schema"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    # Read schema from file
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    cur.execute(schema_sql)
    conn.commit()
    
    print("✓ Schema created successfully!")
    
    cur.close()
    conn.close()


def run_migrations():
    """รัน migrations"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    # Read migrations from file
    with open('database/migrations.sql', 'r', encoding='utf-8') as f:
        migrations_sql = f.read()
    
    cur.execute(migrations_sql)
    conn.commit()
    
    print("✓ Migrations completed!")
    
    cur.close()
    conn.close()


if __name__ == "__main__":
    print("Starting database setup...\n")
    
    try:
        # Step 1: Initialize database
        init_database()
        
        # Step 2: Create schema
        create_schema()
        
        # Step 3: Run migrations
        run_migrations()
        
        print("\n✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
