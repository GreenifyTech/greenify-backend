import sys
import argparse
from scripts import db_ops, admin_ops

def main():
    parser = argparse.ArgumentParser(description="Greenify Backend Management Scripts")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # DB Commands
    subparsers.add_parser("init_db", help="Initialize database and create tables")
    subparsers.add_parser("check_db", help="Check database connection and tables")
    subparsers.add_parser("fix_db", help="Apply manual database fixes/migrations")
    subparsers.add_parser("seed_db", help="Seed database with initial data")
    inspect_parser = subparsers.add_parser("inspect_db", help="Inspect table structure")
    inspect_parser.add_argument("table", nargs="?", default="orders", help="Table name to inspect")

    # Admin Commands
    reset_parser = subparsers.add_parser("reset_admin", help="Reset or create admin user")
    reset_parser.add_argument("--email", default="admin@greenify.eg", help="Admin email")
    reset_parser.add_argument("--password", default="admin123", help="Admin password")
    
    subparsers.add_parser("check_admins", help="List all admin users")

    args = parser.parse_args()

    if args.command == "init_db":
        db_ops.init_db()
    elif args.command == "check_db":
        db_ops.check_db()
    elif args.command == "fix_db":
        db_ops.fix_db()
    elif args.command == "seed_db":
        db_ops.seed_db()
    elif args.command == "inspect_db":
        db_ops.inspect_table(args.table)
    elif args.command == "reset_admin":
        admin_ops.reset_admin(args.email, args.password)
    elif args.command == "check_admins":
        admin_ops.check_admins()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
