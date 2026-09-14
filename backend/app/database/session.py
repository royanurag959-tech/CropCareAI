from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def ensure_database_schema(eng=None):
    target_engine = eng or engine
    try:
        with target_engine.connect() as conn:
            new_cols_scan = [
                ("confidence_level", "VARCHAR(20) DEFAULT 'high'"),
                ("is_uncertain", "BOOLEAN DEFAULT 0"),
                ("plot_id", "VARCHAR(100)"),
                ("parent_scan_id", "INTEGER"),
                ("risk_score", "INTEGER"),
                ("risk_category", "VARCHAR(50)"),
                ("trend", "VARCHAR(50)"),
                ("farmer_notes", "TEXT"),
                ("short_explanation", "TEXT"),
                ("farm_conditions_summary", "TEXT")
            ]
            for col_name, col_type in new_cols_scan:
                try:
                    conn.execute(text(f"ALTER TABLE scan_history ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                except Exception:
                    pass

            new_cols_expert = [
                ("farmer_question", "TEXT"),
                ("dossier_data", "TEXT")
            ]
            for col_name, col_type in new_cols_expert:
                try:
                    conn.execute(text(f"ALTER TABLE expert_requests ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                except Exception:
                    pass
    except Exception as e:
        print(f"Schema check note: {e}")

# Run automatic migration check
ensure_database_schema(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
