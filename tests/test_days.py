# Import the code to be tested
from adventures.d1y2023 import run as run_d1y2023
from adventures.d2y2023 import run as run_d2y2023


def test_day1():
    """Test day 1."""
    with open("inputs/2023/1.txt") as filename:
        data = filename.read()
    assert run_d1y2023(data) == 54728


def test_day2():
    """Test day 2."""
    with open("inputs/2023/2.txt") as filename:
        data = filename.read()
    assert run_d2y2023(data) == 77021
