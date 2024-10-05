import pytest
from caloriescounter import encodeandsearch

def test_encodeandsearch():
    entrace_data = [{'name': 'בשר עוף טחון טרי', 'weight': 1000}, {'name': 'בצל', 'weight': 200}, {'name': 'ביצה טרייה', 'weight': 100}]
    exit_data = [{'name': 'בשר עוף טחון טרי', 'calories': 1430.0, 'proteins': 174.4, 'caloriesfor100': 143, 'proteinsfor100': 17.44}, {'name': 'בצל', 'calories': 80.0, 'proteins': 2.2, 'caloriesfor100': 40, 'proteinsfor100': 1.1}, {'name': 'ביצה טרייה', 'calories': 143.0, 'proteins': 12.560000000000002, 'caloriesfor100': 143, 'proteinsfor100': 12.56}]
    assert encodeandsearch(entrace_data) == exit_data