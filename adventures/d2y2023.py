"""Advent of Code 2023 :: Day 2 :: Cube Conundrum."""

import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)


def run(input: str, verbose: bool = False) -> int:
    """Cube Conundrum.

    Args:
        input (str): Advent of Code input.
        verbose (bool, optional): Print more. Defaults to False.

    Returns:
        int: _description_
    """
    log.info("Going on an adventure!")
    if verbose:
        log.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")

    # Maximum possible cubes of each color
    red: int = 12
    green: int = 13
    blue: int = 14

    valid_games: list[int] = []

    for game in input.splitlines():
        game_id: str = game.split(":")[0].split(" ")[1]
        # Replace color names with the number of max cubes
        rounds: list[str] = (
            game.split(":")[1]
            .replace("red", str(red))
            .replace("green", str(green))
            .replace("blue", str(blue))
            .split(";")
        )
        log.debug(f"Game: {game_id} - {rounds}")

        valid = True
        # Check if the number withdrawn is less than the maximum
        for round in rounds:
            for draw in round.split(","):
                _, _, max_cubes = draw.split(" ")
                if int(max_cubes) < int(draw.split(" ")[1]):
                    valid = False
                    break
            if not valid:
                break

        if valid:
            valid_games.append(int(game_id))

    log.info(f"Valid Games: {sum(valid_games)}")

    score: int = 0
    for game in input.splitlines():
        minimums: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
        # Remove spaces from the game
        game = game.replace(" ", "")
        rounds = game.split(":")[1].split(";")
        for round in rounds:
            rolls = round.split(",")
            for roll in rolls:
                log.debug(f"Roll: {roll}")
                for dice in minimums.keys():
                    if dice in roll:
                        roll = roll.replace(dice, "")
                        value = int(roll)
                        if value > minimums[dice]:
                            minimums[dice] = value
        log.debug(f"Minimums: {minimums}")
        score += minimums["red"] * minimums["green"] * minimums["blue"]
    log.info(f"Score: {score}")
    log.info("Quest complete!")
    return score
