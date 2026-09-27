# Roulette Tracker CLI

Record spins and analyze a European roulette wheel:

```bash
python -m pip install -r requirements.txt
python main.py --spin 17 --spin 0 --spin 32
python main.py --spin 17 --report --min-spins 100
```

The library can also be used directly:

```python
from src.analyzer import RouletteAnalyzer
from src.bet import BetType

tracker = RouletteAnalyzer()
tracker.add_bet(BetType.RED, None, 10, spin_number=1)
tracker.add_spin(17)
print(tracker.get_statistics())
print(tracker.detect_bias())
```

## Interpreting bias results

The analyzer compares observed results with the expected European-wheel distribution (37 pockets). It uses a chi-square test and reports a possible bias only when enough data is available. A low p-value does not guarantee future winnings: repeated testing, random variation, recording errors, and changing wheels can all produce misleading signals. Use this as a historical analysis and logging tool, not as a betting guarantee.
