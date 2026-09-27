import sqlite3
import os
import sys

def migrate_sqlite():
    db_path = os.path.join(os.path.dirname(__file__), 'nutriguard.db')
    if not os.path.exists(db_path):
        print("nutriguard.db does not exist yet.")
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
            
    # Check if meal_plans table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meal_plans'")
    if not cur.fetchone():
        print("Creating meal_plans table...")
        cur.execute("""
            CREATE TABLE meal_plans (
                id CHAR(36) PRIMARY KEY,
                user_id CHAR(36) NOT NULL,
                plan_date DATE NOT NULL,
                plan_type VARCHAR,
                is_ai_generated BOOLEAN,
                safety_validated BOOLEAN,
                targets_snapshot JSON,
                gap_report JSON,
                created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        cur.execute("CREATE INDEX ix_meal_plans_user_id ON meal_plans(user_id)")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meal_plan_meals'")
    if not cur.fetchone():
        print("Creating meal_plan_meals table...")
        cur.execute("""
            CREATE TABLE meal_plan_meals (
                id CHAR(36) PRIMARY KEY,
                plan_id CHAR(36) NOT NULL,
                meal_type VARCHAR NOT NULL,
                day_number INTEGER,
                foods JSON NOT NULL,
                total_nutrition JSON,
                rationale JSON,
                FOREIGN KEY (plan_id) REFERENCES meal_plans(id) ON DELETE CASCADE
            )
        """)

    con.commit()
    con.close()
    print("SQLite migration check complete.")

if __name__ == "__main__":
    migrate_sqlite()
    from data.seed import run_seed
    run_seed()
