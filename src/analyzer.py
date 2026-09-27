"""High-level facade joining wheel, bets, and statistics."""

from typing import Dict

from .bet import BetTracker, BetType
from .stats import BiasDetector
from .wheel import Wheel


class RouletteAnalyzer:
    def __init__(self, min_spins: int = 100):
        self.wheel = Wheel()
        self.bets = BetTracker()
        self.bias = BiasDetector(min_spins=min_spins)

    def add_spin(self, number: int, color: str = None) -> Dict:
        spin = self.wheel.add_spin(number, color)
        self.bets.settle_spin(spin["spin_number"], spin)
        return spin

    def add_bet(self, bet_type, value, amount: float, spin_number: int = None):
        if isinstance(bet_type, str):
            bet_type = BetType(bet_type.lower())
        target_spin = spin_number or (self.wheel.spin_count + 1)
        if amount <= 0:
            raise ValueError("Bet amount must be greater than zero")
        return self.bets.place_bet(bet_type, value, amount, target_spin)

    def get_statistics(self) -> Dict:
        return {"wheel": self.wheel.get_statistics(), "bets": self.bets.get_statistics()}

    def detect_bias(self) -> Dict:
        return self.bias.report(self.wheel.get_spin_history())
