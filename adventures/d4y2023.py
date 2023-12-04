"""Advent of Code :: Day X."""
from adventures.cli.cli import log


def run(input: str = "") -> int:
    """Adventure Template.

    Args:
        input (str, optional): Advent Input. Defaults to "".

    Returns:
        int: Advent Solution.
    """
    log.debug("Running adventure...")
    scratchcards: dict[int, int] = {}
    for i in range(len(input.splitlines())):
        scratchcards[i + 1] = 1
    winnings: int = 0
    for card in input.splitlines():
        card_id = int(card.split(":")[0].split(" ")[-1])

        winning_numbers: list[int] = []
        our_numbers: list[int] = []
        card_numbers = card.split(":")[1]
        winning_numbers = [
            int(number)
            for number in card_numbers.split("|")[0].split(" ")
            if number != ""
        ]
        our_numbers = [
            int(number)
            for number in card_numbers.split("|")[1].split(" ")
            if number != ""
        ]

        winners: int = 0
        for our_number in our_numbers:
            if our_number in winning_numbers:
                winners = winners + 1
        if winners > 0:
            winnings = winnings + 2 ** (winners - 1)
            for _ in range(0, scratchcards[card_id]):
                for idx in range(card_id + 1, card_id + winners + 1):
                    try:
                        scratchcards[idx] = scratchcards[idx] + 1
                    except KeyError:
                        pass
        log.debug(f"Card: {card_id} - Winners - {winners} - Winnings: {winnings}")

    log.info(f"Winnings: {winnings}")
    log.info(f"Scratchcards Sum: {sum(scratchcards.values())}")
    log.debug(f"Input: \n{input}")
    return winnings
