import sys
from sqlalchemy import inspect
from app.database import engine, Base
import app.models  # This imports all models from the __init__.py

def verify_and_create_tables():
    # Inspect existing tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print("Existing tables BEFORE create_all:", existing_tables)

    print("Running Base.metadata.create_all()... this will safely create missing tables like user_profiles.")
    Base.metadata.create_all(bind=engine)

    # Inspect again to verify
    inspector = inspect(engine)
    final_tables = inspector.get_table_names()
    print("Tables AFTER create_all:", final_tables)
    
    missing = []
    required_tables = ['users', 'products', 'categories', 'orders', 'cart', 'user_profiles']
    for req in required_tables:
        if req not in final_tables:
            missing.append(req)
            
    if missing:
        print("ERROR: Models failed to create these tables:", missing)
    else:
        print("SUCCESS: All required tables exist!")

if __name__ == "__main__":
    verify_and_create_tables()
