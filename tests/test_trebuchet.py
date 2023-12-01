from pathlib import Path

from adventures.trebuchet import calibrate


def test_calibrate():
    assert calibrate(Path("inputs/d1-trebuchet-test.txt")) == 281
