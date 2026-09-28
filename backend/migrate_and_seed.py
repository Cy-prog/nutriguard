"""
NutriGuard Production Migration & Seed Script
===============================================
Production workflow:
  1. Run Alembic migrations (alembic upgrade head) for PostgreSQL
  2. For SQLite, use create_all as Alembic is overkill for dev
  3. Run idempotent seed data
  4. Start FastAPI (handled by start.sh)
"""
import os
import sys
import subprocess

def run_migrations():
    """Run appropriate migration strategy based on database type."""
    from core.database import SQLALCHEMY_DATABASE_URL, engine, init_db
    
    if "sqlite" in SQLALCHEMY_DATABASE_URL:
        print("SQLite detected — using create_all for schema.")
        init_db()
        _migrate_sqlite_extras()
    else:
        print("PostgreSQL detected — running Alembic migrations...")
        try:
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__),
                timeout=120
            )
            if result.returncode != 0:
                print(f"Alembic migration output: {result.stdout}")
                print(f"Alembic migration errors: {result.stderr}")
                # Fall back to create_all if alembic fails (e.g. first deployment)
                print("Alembic failed — falling back to create_all for initial schema...")
                init_db()
            else:
                print(f"Alembic migration successful: {result.stdout.strip()}")
        except FileNotFoundError:
            print("Alembic not found — using create_all as fallback.")
            init_db()
        except subprocess.TimeoutExpired:
            print("Alembic timed out — using create_all as fallback.")
            init_db()


def _migrate_sqlite_extras():
    """Add columns/tables that may be missing in older SQLite databases."""
    import sqlite3
    
    db_path = os.path.join(os.path.dirname(__file__), 'nutriguard.db')
    if not os.path.exists(db_path):
        print("nutriguard.db does not exist yet — will be created by create_all.")
        return
        
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Check food columns
    cur.execute("PRAGMA table_info(foods)")
    existing_cols = {r[1] for r in cur.fetchall()}
    
    cols_to_add = [
        ("glycemic_index", "INTEGER"),
        ("purine_level", "VARCHAR"),
        ("vitamin_k_mcg", "NUMERIC"),
        ("nutrient_source", "VARCHAR"),
    ]
    
    for col_name, col_type in cols_to_add:
        if col_name not in existing_cols:
            print(f"Adding column {col_name} ({col_type}) to foods table...")
            cur.execute(f"ALTER TABLE foods ADD COLUMN {col_name} {col_type};")

    con.commit()
    con.close()
    print("SQLite migration check complete.")


def run_seed():
    """Run idempotent seed operations."""
    from data.seed import run_seed as seed_all
    seed_all()


if __name__ == "__main__":
    print("=== NutriGuard Migration & Seed ===")
    run_migrations()
    run_seed()
    print("=== Migration & Seed Complete ===")
