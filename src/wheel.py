"""
Wheel State Management Module

Tracks spin history, frequency distributions, and wheel statistics.
"""

from datetime import datetime
from typing import List, Dict, Tuple
from collections import Counter
import json


class Wheel:
    """Manages roulette wheel state and spin tracking."""
    
    # Standard European roulette wheel: 0-36 (37 numbers)
    EUROPEAN_NUMBERS = list(range(37))
    
    # Color mapping for European roulette
    COLOR_MAP = {
        0: 'green',
        1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black',
        7: 'red', 8: 'black', 9: 'red', 10: 'black', 11: 'black', 12: 'red',
        13: 'black', 14: 'red', 15: 'black', 16: 'red', 17: 'black', 18: 'red',
        19: 'red', 20: 'black', 21: 'red', 22: 'black', 23: 'red', 24: 'black',
        25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red',
        31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black', 36: 'red'
    }
    
    def __init__(self):
        """Initialize wheel with empty spin history."""
        self.spins: List[Dict] = []
        self.spin_count = 0
        self.start_time = datetime.now()
    
    def add_spin(self, number: int, color: str = None, timestamp: datetime = None) -> Dict:
        """
        Record a spin result.
        
        Args:
            number: Winning number (0-36)
            color: Color of number (red/black/green). Auto-detected if not provided.
            timestamp: Spin timestamp. Uses current time if not provided.
        
        Returns:
            Dict with spin details
        """
        if number not in self.EUROPEAN_NUMBERS:
            raise ValueError(f"Invalid number: {number}. Must be 0-36.")
        
        if color is None:
            color = self.COLOR_MAP[number]
        
        if timestamp is None:
            timestamp = datetime.now()
        
        self.spin_count += 1
        spin_record = {
            'spin_number': self.spin_count,
            'number': number,
            'color': color,
            'timestamp': timestamp,
            'is_even': (number % 2 == 0) and (number != 0),
            'is_odd': (number % 2 == 1),
            'is_high': 19 <= number <= 36,
            'is_low': 1 <= number <= 18,
            'dozen': (number - 1) // 12 + 1 if number > 0 else None,
            'column': ((number - 1) % 3) + 1 if number > 0 else None
        }
        
        self.spins.append(spin_record)
        return spin_record
    
    def get_spin_history(self) -> List[Dict]:
        """Return all recorded spins."""
        return self.spins.copy()
    
    def get_frequency_distribution(self) -> Dict[int, int]:
        """Return frequency count of each number."""
        numbers = [spin['number'] for spin in self.spins]
        return dict(sorted(Counter(numbers).items()))
    
    def get_color_distribution(self) -> Dict[str, int]:
        """Return frequency count by color."""
        colors = [spin['color'] for spin in self.spins]
        return dict(Counter(colors))
    
    def get_expected_frequency(self) -> Dict[int, float]:
        """
        Calculate expected frequency for each number.
        
        Returns:
            Dict with expected frequency for each number
        """
        if self.spin_count == 0:
            return {num: 0 for num in self.EUROPEAN_NUMBERS}
        
        expected = self.spin_count / 37  # 37 numbers on European wheel
        return {num: expected for num in self.EUROPEAN_NUMBERS}
    
    def get_deviation(self) -> Dict[int, float]:
        """
        Calculate deviation from expected frequency.
        
        Returns:
            Dict with deviation (actual - expected) for each number
        """
        freq = self.get_frequency_distribution()
        expected = self.get_expected_frequency()
        
        deviation = {}
        for num in self.EUROPEAN_NUMBERS:
            actual = freq.get(num, 0)
            deviation[num] = actual - expected[num]
        
        return deviation
    
    def get_statistics(self) -> Dict:
        """Return comprehensive wheel statistics."""
        if self.spin_count == 0:
            return {
                'total_spins': 0,
                'uptime': 0,
                'frequency_distribution': {},
                'color_distribution': {},
                'most_common': None,
                'least_common': None
            }
        
        freq = self.get_frequency_distribution()
        colors = self.get_color_distribution()
        
        most_common_num = max(freq.items(), key=lambda x: x[1])
        least_common_num = min(freq.items(), key=lambda x: x[1])
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'total_spins': self.spin_count,
            'uptime_seconds': uptime,
            'frequency_distribution': freq,
            'color_distribution': colors,
            'most_common_number': most_common_num[0],
            'most_common_count': most_common_num[1],
            'least_common_number': least_common_num[0],
            'least_common_count': least_common_num[1],
            'average_frequency': self.spin_count / 37
        }
    
    def export_spins(self, filename: str) -> None:
        """Export spin history to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.spins, f, default=str, indent=2)
    
    def import_spins(self, filename: str) -> None:
        """Import spin history from JSON file."""
        with open(filename, 'r') as f:
            spins = json.load(f)
            for spin in spins:
                spin['timestamp'] = datetime.fromisoformat(spin['timestamp'])
                self.spins.append(spin)
            self.spin_count = len(self.spins)
