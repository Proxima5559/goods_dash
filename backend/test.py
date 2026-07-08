import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

async def force_create():
    url = os.getenv("DATABASE_URL")
    
    # 1. Strip out the SQLAlchemy +asyncpg dialect so raw asyncpg can read it
    clean_url = url.replace("+asyncpg", "")
    
    # 2. Redirect to the default 'postgres' database to check the cluster
    base_url = clean_url.split("/")[0] + "//" + clean_url.split("//")[1].split("/")[0] + "/postgres"
    
    print(f"Connecting directly to: {base_url}")
    
    try:
        conn = await asyncpg.connect(base_url)
        
        # Check what databases are actually here
        databases = await conn.fetch("SELECT datname FROM pg_database;")
        existing_dbs = [db['datname'] for db in databases]
        
        print(f"Databases Python can see right now: {existing_dbs}")
        
        if "dash_chart_db" not in existing_dbs:
            print("Target DB not found on this instance! Creating it natively now...")
            await conn.execute("CREATE DATABASE dash_chart_db;")
            print("🚀 Successfully created 'dash_chart_db' on this instance!")
        else:
            print("Wait, 'dash_chart_db' already exists on this server instance!")
            
        await conn.close()
        
    except Exception as e:
        print(f"Error during connection: {e}")

asyncio.run(force_create())