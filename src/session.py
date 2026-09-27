"""Session persistence helpers."""

import json
from datetime import datetime
from typing import Dict

from .analyzer import RouletteAnalyzer


class Session:
    def __init__(self, name: str = "default", min_spins: int = 100):
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.analyzer = RouletteAnalyzer(min_spins=min_spins)

    def save(self, filename: str) -> None:
        payload = {"name": self.name, "created_at": self.created_at, "spins": self.analyzer.wheel.get_spin_history()}
        with open(filename, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, default=str, indent=2)

    @classmethod
    def load(cls, filename: str, min_spins: int = 100):
        with open(filename, encoding="utf-8") as stream:
            payload = json.load(stream)
        session = cls(payload.get("name", "default"), min_spins)
        for spin in payload.get("spins", []):
            session.analyzer.add_spin(spin["number"], spin.get("color"))
        return session
