"""
Bet Tracking and Settlement Module

Records bets, calculates outcomes, and tracks ROI.
"""

from datetime import datetime
from typing import List, Dict, Tuple
from enum import Enum


class BetType(Enum):
    """Supported bet types in roulette."""
    STRAIGHT = "straight"  # Single number
    SPLIT = "split"  # Two adjacent numbers
    STREET = "street"  # Three numbers in a row
    CORNER = "corner"  # Four numbers in a square
    FIVE = "five"  # 0-1-2-3-4 only
    LINE = "line"  # Six numbers
    DOZEN = "dozen"  # 12 numbers (1-12, 13-24, 25-36)
    COLUMN = "column"  # 12 numbers (vertical)
    RED = "red"  # All red numbers
    BLACK = "black"  # All black numbers
    EVEN = "even"  # All even numbers
    ODD = "odd"  # All odd numbers
    HIGH = "high"  # 19-36
    LOW = "low"  # 1-18


class Bet:
    """Represents a single bet."""
    
    # Payout multipliers for each bet type
    PAYOUTS = {
        BetType.STRAIGHT: 36,
        BetType.SPLIT: 18,
        BetType.STREET: 12,
        BetType.CORNER: 9,
        BetType.FIVE: 7,
        BetType.LINE: 6,
        BetType.DOZEN: 3,
        BetType.COLUMN: 3,
        BetType.RED: 2,
        BetType.BLACK: 2,
        BetType.EVEN: 2,
        BetType.ODD: 2,
        BetType.HIGH: 2,
        BetType.LOW: 2,
    }
    
    def __init__(self, bet_type: BetType, value, amount: float, spin_number: int, timestamp: datetime = None):
        """
        Create a bet.
        
        Args:
            bet_type: Type of bet (BetType enum)
            value: What the bet is on (number, color, etc.)
            amount: Bet amount in currency units
            spin_number: Which spin this bet is placed on
            timestamp: When the bet was placed
        """
        self.bet_type = bet_type
        self.value = value
        self.amount = amount
        self.spin_number = spin_number
        self.timestamp = timestamp or datetime.now()
        self.result = None
        self.payout = 0
        self.net_result = 0
    
    def settle(self, spin_result: Dict) -> Tuple[bool, float]:
        """
        Settle the bet based on spin result.
        
        Args:
            spin_result: Dict with 'number', 'color', etc.
        
        Returns:
            Tuple of (won: bool, payout: float)
        """
        won = self._check_win(spin_result)
        
        if won:
            self.payout = self.amount * (self.PAYOUTS[self.bet_type] + 1)
            self.net_result = self.payout - self.amount
            self.result = "WIN"
        else:
            self.payout = 0
            self.net_result = -self.amount
            self.result = "LOSS"
        
        return won, self.payout
    
    def _check_win(self, spin_result: Dict) -> bool:
        """Check if bet wins based on spin result."""
        number = spin_result['number']
        color = spin_result['color']
        
        if self.bet_type == BetType.STRAIGHT:
            return number == self.value
        
        elif self.bet_type == BetType.RED:
            return color == 'red'
        
        elif self.bet_type == BetType.BLACK:
            return color == 'black'
        
        elif self.bet_type == BetType.ODD:
            return number % 2 == 1
        
        elif self.bet_type == BetType.EVEN:
            return number % 2 == 0 and number != 0
        
        elif self.bet_type == BetType.HIGH:
            return 19 <= number <= 36
        
        elif self.bet_type == BetType.LOW:
            return 1 <= number <= 18
        
        elif self.bet_type == BetType.DOZEN:
            dozen = (number - 1) // 12 + 1 if number > 0 else 0
            return dozen == self.value
        
        elif self.bet_type == BetType.COLUMN:
            column = ((number - 1) % 3) + 1 if number > 0 else 0
            return column == self.value
        
        return False
    
    def __repr__(self) -> str:
        return f"Bet({self.bet_type.value}, {self.value}, ${self.amount}, Spin #{self.spin_number})"


class BetTracker:
    """Manages all bets and tracks results."""
    
    def __init__(self):
        """Initialize bet tracker."""
        self.bets: List[Bet] = []
        self.settled_bets: List[Bet] = []
        self.open_bets: List[Bet] = []
    
    def place_bet(self, bet_type: BetType, value, amount: float, spin_number: int) -> Bet:
        """
        Place a new bet.
        
        Args:
            bet_type: Type of bet
            value: What the bet is on
            amount: Bet amount
            spin_number: Which spin this bet is on
        
        Returns:
            Bet object
        """
        bet = Bet(bet_type, value, amount, spin_number)
        self.bets.append(bet)
        self.open_bets.append(bet)
        return bet
    
    def settle_bet(self, bet: Bet, spin_result: Dict) -> Tuple[bool, float]:
        """
        Settle a specific bet.
        
        Args:
            bet: Bet to settle
            spin_result: Spin result dict
        
        Returns:
            Tuple of (won: bool, payout: float)
        """
        won, payout = bet.settle(spin_result)
        
        if bet in self.open_bets:
            self.open_bets.remove(bet)
        self.settled_bets.append(bet)
        
        return won, payout
    
    def settle_spin(self, spin_number: int, spin_result: Dict) -> Dict:
        """
        Settle all bets for a specific spin.
        
        Args:
            spin_number: Spin number
            spin_result: Spin result dict
        
        Returns:
            Settlement summary dict
        """
        spin_bets = [b for b in self.open_bets if b.spin_number == spin_number]
        
        total_wagered = sum(b.amount for b in spin_bets)
        total_payout = 0
        wins = 0
        losses = 0
        
        for bet in spin_bets:
            won, payout = self.settle_bet(bet, spin_result)
            total_payout += payout
            if won:
                wins += 1
            else:
                losses += 1
        
        return {
            'spin_number': spin_number,
            'bets_settled': len(spin_bets),
            'wins': wins,
            'losses': losses,
            'total_wagered': total_wagered,
            'total_payout': total_payout,
            'net_result': total_payout - total_wagered
        }
    
    def get_statistics(self) -> Dict:
        """Return betting statistics."""
        if not self.settled_bets:
            return {
                'total_bets': 0,
                'total_wagered': 0,
                'total_payout': 0,
                'total_win_loss': 0,
                'win_rate': 0,
                'roi': 0
            }
        
        wins = sum(1 for b in self.settled_bets if b.result == "WIN")
        losses = sum(1 for b in self.settled_bets if b.result == "LOSS")
        
        total_wagered = sum(b.amount for b in self.settled_bets)
        total_payout = sum(b.payout for b in self.settled_bets)
        net_result = total_payout - total_wagered
        
        win_rate = wins / len(self.settled_bets) if self.settled_bets else 0
        roi = (net_result / total_wagered * 100) if total_wagered > 0 else 0
        
        return {
            'total_bets': len(self.settled_bets),
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_wagered': total_wagered,
            'total_payout': total_payout,
            'total_win_loss': net_result,
            'roi_percent': roi,
            'average_bet': total_wagered / len(self.settled_bets) if self.settled_bets else 0
        }
