from pathlib import Path

from adventures.d1y2023 import run


def test_calibrate():
    assert run(Path("inputs/2023/1.txt")) == 54728
