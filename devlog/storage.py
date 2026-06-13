import json
import uuid
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path.home() / ".devlog" / "logs.json"


def _load():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(entries):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def add_entry(message, tags=None):
    entries = _load()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().isoformat(),
        "date": date.today().isoformat(),
        "message": message,
        "tags": tags or [],
    }
    entries.append(entry)
    _save(entries)
    return entry


def get_by_date(target_date):
    return [e for e in _load() if e["date"] == target_date.isoformat()]


def get_range(start_date, end_date):
    return [
        e for e in _load()
        if start_date.isoformat() <= e["date"] <= end_date.isoformat()
    ]


def delete_entry(entry_id):
    entries = _load()
    filtered = [e for e in entries if not e["id"].startswith(entry_id)]
    if len(filtered) == len(entries):
        return False
    _save(filtered)
    return True
