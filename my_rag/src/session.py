"""Session management for terminal RAG conversations."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class Session:
    """Manages conversation history and session persistence."""

    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.created_at = datetime.now()
        self.saved = True
        self.current_file: Optional[str] = None

    def append(self, query: str, response: str, sources: Optional[List[Dict]] = None):
        """Add a query/response pair to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response
        }
        if sources:
            entry["sources"] = sources
        self.history.append(entry)
        self.saved = False

    def save_to_file(self, filename: str) -> bool:
        """Save session to JSON file in sessions/ directory."""
        try:
            sessions_dir = Path("sessions")
            sessions_dir.mkdir(exist_ok=True)

            filepath = sessions_dir / f"{filename}.json"

            data = {
                "created_at": self.created_at.isoformat(),
                "saved_at": datetime.now().isoformat(),
                "conversation_count": len(self.history),
                "history": self.history
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.saved = True
            self.current_file = filename
            return True
        except Exception as e:
            return False

    def load_from_file(self, filename: str) -> bool:
        """Load session from JSON file."""
        try:
            sessions_dir = Path("sessions")
            filepath = sessions_dir / f"{filename}.json"

            if not filepath.exists():
                return False

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.history = data.get("history", [])
            self.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
            self.saved = True
            self.current_file = filename
            return True
        except Exception as e:
            return False

    def clear(self):
        """Clear conversation history."""
        self.history = []
        self.saved = True

    def get_formatted_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history, optionally limited to last n entries."""
        if limit:
            return self.history[-limit:]
        return self.history

    def generate_filename(self) -> str:
        """Generate a timestamped filename for auto-save."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all available session files with metadata."""
        sessions_dir = Path("sessions")
        if not sessions_dir.exists():
            return []

        sessions = []
        for filepath in sessions_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                sessions.append({
                    "filename": filepath.stem,
                    "created_at": data.get("created_at", "Unknown"),
                    "saved_at": data.get("saved_at", "Unknown"),
                    "conversation_count": data.get("conversation_count", 0)
                })
            except Exception:
                continue

        return sorted(sessions, key=lambda x: x.get("saved_at", ""), reverse=True)

    def get_context_window(self, n: int) -> List[Dict[str, str]]:
        """Get last n conversation turns for context window."""
        if n <= 0:
            return []

        # Return last n turns, or all if n is larger than history
        return self.history[-n:] if len(self.history) > n else self.history

