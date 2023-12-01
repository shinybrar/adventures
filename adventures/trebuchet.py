"""Advent of Code Day 1: Trebuchet?

The problem description can be found at https://adventofcode.com/2023/day/1
"""
from pathlib import Path


def calibrate(input: Path, verbose: bool = False) -> int:
    """Calibrate the trebuchet.

    Args:
        input (Path): Path to the input file.
        verbose (bool, optional): Print more. Defaults to False.
    """
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
    # Open the file for reading.
    with open(input) as data:
        # Read the file contents.
        contents = data.read()
        # Start reading the line by each character and replace the words with numbers.
        for line in contents.splitlines():
            original: str = line
            # Search and replace all combinations in the line.
            for combination in combinations.keys():
                if combination in line:
                    line = line.replace(combination, combinations[combination])
            # Search and replace all numbers in the line.
            for number in numbers.keys():
                if number in line:
                    line = line.replace(number, numbers[number])
            # Remove all non-digits characters from the line
            for character in line:
                if not character.isdigit():
                    line = line.replace(character, "")
            # Calculate the calibration value of the line.
            calibration: int = int(line[0] + line[-1])
            if verbose:
                print(original, line, calibration)
            calibrations.append(calibration)
    # Print the sum of the calibrations.
    print(f"Sum of calibrations: {sum(calibrations)}")
    return sum(calibrations)


if __name__ == "__main__":
    calibrate(Path("inputs/d1-trebuchet.txt"), verbose=False)
