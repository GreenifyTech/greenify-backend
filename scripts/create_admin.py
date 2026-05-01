import argparse
import sys
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def print_sql_fallback(email: str, hashed: str) -> None:
    print("\n" + "=" * 70)
    print("SQL FALLBACK -- paste this into the Supabase SQL Editor:")
    print("=" * 70)
    print(f"""
UPDATE users
SET
    password    = '{hashed}',
    is_admin    = TRUE,
    is_active   = TRUE,
    role        = 'admin'
WHERE email = '{email}';

-- If user does not exist:
-- INSERT INTO users (full_name, email, password, role, is_admin, is_active)
-- VALUES ('Admin User', '{email}', '{hashed}', 'admin', TRUE, TRUE);
""")
    print("=" * 70)
    print("IMPORTANT: The hash above is one-time generated.")
    print("=" * 70 + "\n")

def run(email: str, password: str, sql_only: bool = False) -> None:
    hashed = hash_password(password)

    print(f"\n[SUCCESS] bcrypt hash generated for: {email}")
    print(f"   Hash: {hashed}\n")

    print_sql_fallback(email, hashed)

    if sql_only:
        return

    try:
        from scripts.utils import get_db
        from app.models.user import User

        with get_db() as db:
            admin = db.query(User).filter(User.email == email).first()

            if admin:
                admin.password = hashed
                admin.is_admin = True
                admin.is_active = True
                admin.role = "admin"
                db.commit()
                print(f"[SUCCESS] Admin '{email}' password reset successfully.")
            else:
                new_admin = User(
                    full_name="Admin User",
                    email=email,
                    password=hashed,
                    role="admin",
                    is_admin=True,
                    is_active=True,
                )
                db.add(new_admin)
                db.commit()
                print(f"[SUCCESS] New admin user '{email}' created.")

    except Exception as exc:
        print(f"\n[ERROR] Database connection failed: {exc}")
        print("   -> Use the SQL fallback printed above to fix the admin manually.")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Create or reset admin user.")
    parser.add_argument("--email", default="admin@greenify.eg")
    parser.add_argument("--password", default="Admin@Greenify2024!")
    parser.add_argument("--sql-only", action="store_true")
    args = parser.parse_args()

    print(f"\nGreenify Admin Setup: {args.email}")
    run(email=args.email, password=args.password, sql_only=args.sql_only)

if __name__ == "__main__":
    main()
