"""CLI for adventures."""
from datetime import datetime
from os import environ
from pathlib import Path

import click
import requests

now = datetime.now()


@click.command("get", help="Get input for new adventure")
@click.option(
    "-d",
    "--day",
    default=now.day,
    show_default=True,
    help="day of the adventure, default is today",
)
@click.option(
    "-y",
    "--year",
    default=now.year,
    show_default=True,
    help="year of the adventure, default is this year",
)
@click.option(
    "--save-path",
    default=f"inputs/{now.year}/{now.day}.txt",
    show_default=True,
    help="path to save the adventure input file",
)
@click.option(
    "--url",
    default=f"https://adventofcode.com/{now.year}/day/{now.day}/input",
    show_default=True,
    help="url",
)
@click.option(
    "--session",
    default=environ.get("AOC_SESSION", None),
    envvar="AOC_SESSION",
    show_default=False,
    help="session cookie for adventofcode.com",
)
def get(day: int, year: int, save_path: str, url: str, session: str):
    """Get input for new adventure.

    Args:
        day (int): Day of the adventure, default is today
        year (int): Year of the adventure, default is this year
        save_path (str): Path to save the adventure input file
        url (str): URL
        session (str): Session cookie for adventofcode.com
    """
    click.echo(f"Getting a new adventure for Dec {day}, {year}...")
    click.echo(f"Saving to {save_path}...")
    click.echo(f"Getting input from {url}...")

    # If the path does not exist, create it.
    path: Path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, cookies={"session": session})
    response.raise_for_status()
    click.echo(f"Writing to {save_path}...")
    with open(save_path, "wb") as f:
        f.write(response.content)
    click.echo("Done!")


@click.group()
def cli():
    """CLI for adventures."""
    pass


cli.add_command(get)

if __name__ == "__main__":
    cli()
