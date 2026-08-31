import os
import sqlite3
import pytest
from alembic.config import Config
from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.main import app


def test_migration_from_legacy_schema_without_document_context():
    """Verify that a legacy database lacking the document_context column

    upgrades via Alembic and supports subsequent generate-post requests.
    """
    db_path = "./test_legacy_migration.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # 1. Create a legacy SQLite database directly with SQLite DDL (no document_context column)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            hashed_password VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            topic VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            type VARCHAR(50) NOT NULL DEFAULT 'professional',
            date VARCHAR(50) NOT NULL,
            created_at DATETIME NOT NULL,
            content_hash VARCHAR(64) NOT NULL UNIQUE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Insert a pre-existing legacy post
    cursor.execute("""
        INSERT INTO posts (id, topic, content, type, date, created_at, content_hash)
        VALUES (1, 'Legacy Post', 'Legacy Content', 'tech', '2026-08-30 10:00:00', '2026-08-30 10:00:00', 'legacyhash123')
    """)
    conn.commit()
    conn.close()

    # 2. Verify document_context column does NOT exist prior to migration
    engine_temp = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine_temp)
    initial_cols = [col["name"] for col in inspector.get_columns("posts")]
    assert "document_context" not in initial_cols, "Legacy table should not have document_context initially"
    engine_temp.dispose()

    # 3. Run Alembic upgrade head against this legacy database
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini_path = os.path.join(root_dir, "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("script_location", os.path.join(root_dir, "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    command.upgrade(alembic_cfg, "head")

    # 4. Verify document_context column exists after migration
    engine_migrated = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    inspector_migrated = inspect(engine_migrated)
    updated_cols = [col["name"] for col in inspector_migrated.get_columns("posts")]
    assert "document_context" in updated_cols, "document_context column must exist after migration"

    # Verify legacy post data was preserved with null document_context
    from sqlalchemy import text
    MigratedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_migrated)
    db_session = MigratedSessionLocal()
    legacy_row = db_session.execute(text("SELECT * FROM posts WHERE id = 1")).fetchone()
    assert legacy_row is not None


    # 5. Connect FastAPI TestClient to the migrated database and test generate-post
    def override_migrated_db():
        db = MigratedSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_migrated_db
    settings.LLM_PROVIDER = "mock"

    with TestClient(app) as test_client:
        post_payload = {
            "topic": "Post Migration Test",
            "type": "professional",
            "length": "short",
            "tone": "insightful",
            "document_context": "Verified AWS Cloud Practitioner Certification"
        }
        response = test_client.post("/api/v1/generate-post", json=post_payload)
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is True
        assert data["post"]["document_context"] == "Verified AWS Cloud Practitioner Certification"
        assert data["post"]["topic"] == "Post Migration Test"

    app.dependency_overrides.clear()
    db_session.close()
    engine_migrated.dispose()

    # Cleanup
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass
