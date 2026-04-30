from app.models.user import User
from app.core.security import hash_password
from scripts.utils import get_db

def reset_admin(email="admin@greenify.eg", password="admin123"):
    with get_db() as db:
        admin = db.query(User).filter(User.email == email).first()
        if admin:
            admin.password = hash_password(password)
            admin.is_admin = True
            admin.is_active = True
            db.commit()
            print(f"Admin '{email}' password reset to '{password}'")
        else:
            new_admin = User(
                full_name="Admin User",
                email=email,
                password=hash_password(password),
                role="admin",
                is_admin=True,
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            print(f"Admin user '{email}' created with password '{password}'")

def check_admins():
    with get_db() as db:
        admins = db.query(User).filter(User.is_admin == True).all()
        if not admins:
            print("No admin users found.")
        else:
            print(f"Found {len(admins)} admin users:")
            for admin in admins:
                print(f"- {admin.email} (ID: {admin.id}, Active: {admin.is_active}, Role: {admin.role})")
