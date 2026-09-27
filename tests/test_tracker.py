import pytest

from src.analyzer import RouletteAnalyzer
from src.bet import BetType
from src.wheel import Wheel


def test_wheel_derives_color_and_rejects_invalid_numbers():
    wheel = Wheel()
    assert wheel.add_spin(0)["color"] == "green"
    with pytest.raises(ValueError):
        wheel.add_spin(37)


def test_straight_bet_is_settled_when_spin_is_recorded():
    analyzer = RouletteAnalyzer()
    analyzer.add_bet(BetType.STRAIGHT, 17, 10, spin_number=1)
    analyzer.add_spin(17)
    stats = analyzer.bets.get_statistics()
    assert stats["wins"] == 1
    assert stats["total_win_loss"] == 350


def test_bias_report_requires_configured_sample_size():
    analyzer = RouletteAnalyzer(min_spins=10)
    analyzer.add_spin(1)
    assert analyzer.detect_bias()["chi_square"]["status"] == "INSUFFICIENT_DATA"
