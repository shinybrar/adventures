"""CLI for adventures."""
import importlib
import logging
from datetime import datetime
from os import environ
from pathlib import Path

import click
import requests
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)

now = datetime.now()


@click.command("get", help="Get an adventure")
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
    default="https://adventofcode.com/",
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
    url = f"{url}{year}/day/{day}/input"
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


@click.command("run", help="Run an adventure")
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
    "-v",
    "--verbose",
    default=False,
    is_flag=True,
    show_default=True,
    help="verbose logging",
)
def run(day: int, year: int, verbose: bool):
    """Run an adventure.

    Args:
        day (int): Day of the adventure, default is today
        year (int): Year of the adventure, default is this year
        code (str): Code to run
        input (str): Path to the input file
        verbose (bool): Verbose logging
    """
    if verbose:
        log.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")
    code: str = f"adventures.d{day}y{year}:run"
    input: str = f"inputs/{year}/{day}.txt"
    click.echo(f"Running adventure for Dec {day}, {year}...")
    click.echo(f"Code Import: {code}...")
    # Import the code to run.
    mod, func = code.split(":")
    module = importlib.import_module(mod)
    function = getattr(module, func)
    # Read the input.
    click.echo("Reading input...")
    with open(input) as filename:
        data = filename.read()
    # Run the code.
    click.echo("Running...")
    function(input=data)


@click.group()
def cli():
    """CLI for adventures."""
    pass


cli.add_command(get)
cli.add_command(run)

if __name__ == "__main__":
    cli()
