import os
import json
import hashlib
import sys
from pathlib import Path

# Add project root to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.database import SessionLocal, engine, Base
from backend.app.models import Post


def compute_content_hash(topic: str, content: str, date: str) -> str:
    raw_str = f"{topic.strip()}:{content.strip()}:{date.strip()}"
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()


def migrate_json_data():
    print("=" * 60)
    print("Starting Idempotent Data Migration: JSON -> SQL Database")
    print("=" * 60)

    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    json_paths = [
        ROOT_DIR / "backend" / "post_history.json",
        ROOT_DIR / "post_history.json"
    ]

    history_file = None
    for path in json_paths:
        if path.exists():
            history_file = path
            break

    if not history_file:
        print("No post_history.json file found. Skipping migration.")
        return

    print(f"Reading post history from: {history_file}")

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON history file: {e}")
        return

    if not posts_data or not isinstance(posts_data, list):
        print("JSON file contains no valid post records.")
        return

    db = SessionLocal()
    migrated_count = 0
    skipped_count = 0

    try:
        for item in posts_data:
            topic = item.get("topic", "").strip()
            content = item.get("content", "").strip()
            post_type = item.get("type", "professional").strip()
            date = item.get("date", "").strip()

            if not content:
                continue

            content_hash = compute_content_hash(topic, content, date)

            # Check if post already exists in DB (Idempotency check)
            existing_post = db.query(Post).filter(Post.content_hash == content_hash).first()
            if existing_post:
                skipped_count += 1
                continue

            new_post = Post(
                topic=topic or "General",
                content=content,
                type=post_type or "professional",
                date=date or "N/A",
                content_hash=content_hash,
                user_id=None  # Default/unassigned legacy post
            )
            db.add(new_post)
            migrated_count += 1

        db.commit()
        print(f"Migration completed successfully!")
        print(f"  - Total records in JSON: {len(posts_data)}")
        print(f"  - New posts migrated to DB: {migrated_count}")
        print(f"  - Duplicate posts skipped: {skipped_count}")
        print(f"  - Total posts in DB now: {db.query(Post).count()}")

    except Exception as e:
        db.rollback()
        print(f"Error during database migration: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_json_data()
