from sqlalchemy import text, inspect
from scripts.utils import get_engine
from app.database import Base
import app.models
from app.config import settings

def init_db():
    engine = get_engine()
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print("Existing tables BEFORE create_all:", existing_tables)

    print("Running Base.metadata.create_all()...")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    final_tables = inspector.get_table_names()
    print("Tables AFTER create_all:", final_tables)
    
    required_tables = ['users', 'products', 'categories', 'orders', 'cart_items', 'user_profiles']
    missing = [req for req in required_tables if req not in final_tables]
            
    if missing:
        print("ERROR: Models failed to create these tables:", missing)
    else:
        print("SUCCESS: All required tables exist!")

def check_db():
    engine = get_engine()
    print(f"Connecting to: {settings.database_url}")
    try:
        inspector = inspect(engine)
        print("Tables:", inspector.get_table_names())
    except Exception as e:
        print("Error:", e)

def inspect_table(table_name='orders'):
    engine = get_engine()
    inspector = inspect(engine)
    try:
        columns = inspector.get_columns(table_name)
        print(f"Structure for table: {table_name}")
        for column in columns:
            print(f"Column: {column['name']}, Type: {column['type']}")
    except Exception as e:
        print(f"Error inspecting table {table_name}: {e}")

def fix_db():
    engine = get_engine()
    with engine.begin() as conn:
        # 1. Orders table fixes
        print("Checking Orders table columns...")
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN payment_proof_url VARCHAR(255)"))
            print("Added payment_proof_url")
        except Exception as e:
            pass # Already exists
            
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN payment_verified BOOLEAN DEFAULT 0"))
            print("Added payment_verified")
        except Exception as e:
            pass

        # 2. Users table fixes
        print("Checking Users table columns...")
        try:
            conn.execute(text("ALTER TABLE users MODIFY phone VARCHAR(50)"))
            print("Increased users.phone to VARCHAR(50)")
        except Exception as e:
            pass

        # 3. Products table fixes
        print("Checking Products table columns...")
        try:
            conn.execute(text("ALTER TABLE products CHANGE stock_quantity stock int NOT NULL DEFAULT 0"))
            print("Renamed stock_quantity to stock")
        except Exception as e:
            pass

        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN is_featured tinyint(1) NOT NULL DEFAULT 0 AFTER stock"))
            print("Added is_featured column")
        except Exception as e:
            pass

        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN slug varchar(250) UNIQUE AFTER is_featured"))
            print("Added slug column")
        except Exception as e:
            pass

        # From migrate_medicine.py
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN product_type VARCHAR(50) DEFAULT 'PLANT' NOT NULL"))
            print("Added product_type column")
        except Exception as e:
            pass

        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN target_pest VARCHAR(200) NULL"))
            print("Added target_pest column")
        except Exception as e:
            pass

        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN usage_instructions TEXT NULL"))
            print("Added usage_instructions column")
        except Exception as e:
            pass

        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN phi VARCHAR(100) NULL"))
            print("Added phi column")
        except Exception as e:
            pass

        # Data fixes from fix_db.py
        print("Fixing NULL product_type data...")
        conn.execute(text("UPDATE products SET product_type='PLANT' WHERE product_type IS NULL"))
        print("Data fix complete.")

def seed_db():
    from scripts.utils import get_db
    print("Seeding database with initial data...")
    with get_db() as db:
        try:
            # Check if we already have diseases
            count = db.execute(text("SELECT COUNT(*) FROM diseases")).scalar()
            if count > 0:
                print("Disease data already exists. Skipping disease seed.")
            else:
                db.execute(text("""
                    INSERT INTO diseases (name, symptoms, cause, treatment_keywords, description) 
                    VALUES ('Leaf Spot (Fungal)', 'yellow spots, brown edges, wilting', 'Fungi (Cercospora)', 'Fungicide, Copper', 'A common fungal disease affecting many plants.')
                """))
                print("Disease seed data inserted.")

            # Ensure we have a medicine that matches
            medicine_exists = db.execute(text("SELECT COUNT(*) FROM products WHERE product_type='MEDICINE'")).scalar()
            if medicine_exists > 0:
                print("Medicine products already exist. Skipping medicine seed.")
            else:
                # Check if category 1 exists
                cat_exists = db.execute(text("SELECT COUNT(*) FROM categories WHERE id=1")).scalar()
                if not cat_exists:
                    db.execute(text("INSERT INTO categories (id, name) VALUES (1, 'General')"))
                
                db.execute(text("""
                    INSERT INTO products (category_id, name, price, stock, product_type, target_pest, usage_instructions, phi, slug)
                    VALUES (1, 'BioFungicide Pro', 15.50, 100, 'MEDICINE', 'Fungicide, Mold', 'Mix 10ml per liter of water. Spray weekly.', '3 Days', 'biofungicide-pro')
                """))
                print("Medicine seed data inserted.")
            
            db.commit()
            print("Seeding complete.")
        except Exception as e:
            db.rollback()
            print(f"Error seeding data: {e}")

