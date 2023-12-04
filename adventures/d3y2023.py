"""Advent of Code :: 2023 :: Day 3: Gear Ratios."""
from collections import defaultdict

from adventures.cli.cli import log


def run(input: str = "") -> int:  # noqa: C901
    """Adventure Template.

    Args:
        input (str, optional): Advent Input. Defaults to "".

    Returns:
        int: Advent Solution.
    """
    log.debug("Running the adventure...")

    # Valid represents the locations in the matrix where
    # numbers can be potentially placed
    valid: dict[int, list[int]] = defaultdict(list)
    # Specials represents the locations in the matrix where
    # special characters are located
    specials: dict[int, list[int]] = defaultdict(list)
    # Gears represents the locations in the matrix where
    # gears are located
    gears: dict[int, list[int]] = defaultdict(list)
    # Numbers represents the numbers in the matrix in format
    # {lineno: [(number, start, stop), ...]}
    numbers: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    sum: int = 0
    ratio: int = 0

    # Modify input, to add a line of len(input.splitlines()[0]) dots to the start and end
    input = (
        "." * len(input.splitlines()[0])
        + "\n"
        + input
        + "\n"
        + "." * len(input.splitlines()[0])
    )
    # Also add 3 "." to the start and end of each line,
    # to account for the special characters at edges
    input = "\n".join(["..." + line + "..." for line in input.splitlines()])

    for lineno, line in enumerate(input.splitlines()):
        start: int = 0
        for index, character in enumerate(line):
            if not character.isdigit() and character != ".":
                # This is a special character,
                # which determines the validity of the matrix position
                specials[lineno] = specials[lineno] + [index]
                # Add valid locations to the array.
                valid[lineno] = valid[lineno] + [index - 1, index + 1]
                valid[lineno - 1] = valid[lineno - 1] + [index - 1, index, index + 1]
                valid[lineno + 1] = valid[lineno + 1] + [index - 1, index, index + 1]
            if not character.isdigit() and character == "*":
                # This is a gear, lets record it in the gears array
                gears[lineno] = gears[lineno] + [index]
            if character.isdigit():
                # This character is a digit, so lets record it in our numbers array
                if not line[index - 1].isdigit():
                    # This is the start of a number
                    start = index
                # Check if it is a one digit number
                if (start == index) and not line[index + 1].isdigit():
                    # This is a one digit number
                    numbers[lineno].append((int(line[index]), start, index))
                elif line[index - 1].isdigit() and line[index + 1].isdigit():
                    # This is a continuation of a number from the previous index
                    continue
                elif line[index - 1].isdigit() and not line[index + 1].isdigit():
                    # This is the end of a number
                    numbers[lineno].append(
                        (int(line[start : index + 1]), start, index)  # noqa: E203
                    )

    # Cleanup the valid array
    for key in valid:
        valid[key] = sorted(set(valid[key]))

    # Now we have the valid locations, and also the locations of all the numbers
    # Lets check each number and see if it is valid
    part_added: bool = False
    for index in numbers.keys():
        for number, start, stop in numbers[index]:
            # From the starting index + stop + 1 should be in the valid locations
            part_added = False
            for idx in range(start, stop + 1):
                if idx in valid[index]:
                    # This number is not valid, so remove it from the numbers array
                    if not part_added:
                        log.debug(
                            f"Valid Number: {number}, Line: {index} Loc: {start, stop}"
                        )
                        sum += number
                        part_added = True

    # Gears Ratio Logic
    log.debug("Input:")
    log.debug(input)
    log.debug(f"Gears: {gears}")
    log.debug(f"Numbers: {numbers}")

    for lineno in gears.keys():
        for index in gears[lineno]:
            log.debug(f"Gear: {lineno, index}")
            log.debug(f"Previous Numbers: {numbers[lineno-1]}")
            log.debug(f"Current Numbers: {numbers[lineno]}")
            log.debug(f"Next Numbers: {numbers[lineno+1]}")
            # Check for numbers around the gear in the same line
            locations = [index - 1, index, index + 1]
            parts: list[int] = []
            for number, start, stop in numbers[lineno]:
                log.debug(f"Evaluating: {number, start, stop} from line {lineno}")
                overlap = any(
                    location in range(start, stop + 1) for location in locations
                )
                if overlap:
                    parts.append(number)
                    log.debug(f"Added: {number} from current line {lineno} to {parts}")

            for number, start, stop in numbers[lineno - 1]:
                overlap = any(
                    location in range(start, stop + 1) for location in locations
                )
                if overlap:
                    parts.append(number)
                    log.debug(
                        f"Added: {number} from previous line {lineno-1} to {parts}"
                    )

            for number, start, stop in numbers[lineno + 1]:
                overlap = any(
                    location in range(start, stop + 1) for location in locations
                )
                if overlap:
                    parts.append(number)
                    log.debug(f"Added: {number} from next line {lineno+1} to {parts}")

            log.debug(f"Parts: {parts}")
            if len(parts) == 2:
                # This is a valid gear ratio
                ratio += parts[0] * parts[1]

    log.info(f"Engine Parts: {sum}")
    log.info(f"Gears Ratio : {ratio}")

    return ratio
