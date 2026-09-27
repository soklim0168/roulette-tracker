"""Statistical analysis for a European roulette wheel."""

from collections import Counter
from math import sqrt
from typing import Dict, List

from scipy.stats import chisquare


class BiasDetector:
    """Run descriptive and inferential tests on recorded spin dictionaries."""

    def __init__(self, min_spins: int = 100):
        self.min_spins = min_spins

    def frequency_report(self, spins: List[Dict]) -> Dict:
        counts = Counter(spin["number"] for spin in spins)
        total = len(spins)
        expected = total / 37 if total else 0
        return {
            "spins_analyzed": total,
            "expected_per_number": expected,
            "counts": {str(number): counts.get(number, 0) for number in range(37)},
            "deviation": {str(number): counts.get(number, 0) - expected for number in range(37)},
        }

    def chi_square_test(self, spins: List[Dict], alpha: float = 0.05) -> Dict:
        if len(spins) < self.min_spins:
            return {"status": "INSUFFICIENT_DATA", "minimum_spins": self.min_spins, "spins_analyzed": len(spins)}
        observed = [Counter(s["number"] for s in spins).get(number, 0) for number in range(37)]
        statistic, p_value = chisquare(observed)
        return {
            "status": "COMPLETE",
            "chi2": float(statistic),
            "p_value": float(p_value),
            "alpha": alpha,
            "potential_bias": bool(p_value < alpha),
            "spins_analyzed": len(spins),
            "warning": "A significant result is evidence for further investigation, not proof of a predictable wheel.",
        }

    def hot_cold(self, spins: List[Dict], threshold: float = 2.0) -> Dict:
        if not spins:
            return {"status": "INSUFFICIENT_DATA", "hot": [], "cold": []}
        counts = Counter(s["number"] for s in spins)
        expected = len(spins) / 37
        standard_deviation = sqrt(expected * (1 - 1 / 37))
        hot, cold = [], []
        for number in range(37):
            z = (counts.get(number, 0) - expected) / standard_deviation if standard_deviation else 0
            item = {"number": number, "count": counts.get(number, 0), "z_score": z}
            if z >= threshold:
                hot.append(item)
            elif z <= -threshold:
                cold.append(item)
        return {"status": "COMPLETE", "hot": sorted(hot, key=lambda x: -x["z_score"]), "cold": sorted(cold, key=lambda x: x["z_score"])}

    def report(self, spins: List[Dict]) -> Dict:
        return {"frequency": self.frequency_report(spins), "chi_square": self.chi_square_test(spins), "hot_cold": self.hot_cold(spins)}
