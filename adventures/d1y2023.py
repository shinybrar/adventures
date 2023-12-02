"""Advent of Code 2023 :: Day 1 :: Trebuchet?!."""
import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)


def run(input: str, verbose: bool = True) -> int:
    """Calibrate the trebuchet?!.

    Args:
        input (Path): Path to the input file.
        verbose (bool, optional): Print more. Defaults to False.
    """
    if verbose:
        log.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")
    calibrations: list[int] = []
    numbers: dict[str, str] = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
    }
    combinations: dict[str, str] = {}
    # Create all possible combinations of numbers,
    # which share the same last and first digit.
    for front in numbers.keys():
        for back in numbers.keys():
            if front[-1] == back[0]:
                combinations[front[:-1] + back] = str(numbers[front]) + str(
                    numbers[back]
                )
    for line in input.splitlines():
        original: str = line
        # Search and replace all combinations in the line.
        for combination, replacement in combinations.items():
            line = line.replace(combination, replacement)
        # Search and replace all numbers in the line.
        for number, replacement in numbers.items():
            line = line.replace(number, replacement)
        # Remove all non-digit characters from the line.
        line = "".join(filter(str.isdigit, line))
        # Calculate the calibration value of the line.
        calibration: int = int(line[0] + line[-1])
        log.debug(f"{original} -> {line} -> {calibration}")
        calibrations.append(calibration)

    # Print the sum of the calibrations.
    log.info(f"Sum of calibrations: {sum(calibrations)}")
    return sum(calibrations)
