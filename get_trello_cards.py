# This script gets the number of cards for a particular Trello board
# uses CURL requests to pull data using the Trello API
# see https://stateful.com/blog/trello-api-examples
# https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/
#
# To automate this script with a CRON job, it's advised to store your Trello API creds
# in a secure folder e.g. /root/trello_credentials containing the following variables:
# TRELLO_API_KEY=xxxxxxxxxxxx
# TRELLO_API_TOKEN=xxxxxxxxxxxx
# TRELLO_BOARD_ID=xxxxxxxxxxxx
# Your Trello board id can be found by putting '.json' at end of the Trello board URL
# in your browser.
# Then run this script as root/sudo user so the script can pull in the
# trello_credentials correctly.
# e.g.
# sudo poetry run python get_trello_cards.py
#
# Created by jstucken 9/2/2023

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pytz
import requests
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

console = Console()

TRELLO_CREDENTIALS_PATH = Path("/root/trello_api_credentials")


class InvalidRequestResponse(Exception):
    """Custom error handler for when a request response is not successful"""


class InvalidCredentialsFile(Exception):
    """Custom error handler for when credentials file cannot be loaded"""


class TrelloScraper:
    # Trello API base url
    base_url = "https://api.trello.com"

    def __init__(self, api_key: str, api_token: str):
        # params which will be used for API requests
        self.api_params = {"key": api_key, "token": api_token}

    def get_trello_json(self, endpoint: str) -> dict:
        """Runs a CURL request to Trello and returns json in dictionary format"""
        response = requests.get(self.base_url + endpoint, self.api_params)

        # confirm that response was successful
        # response code 200 = success
        if response.status_code != 200:
            # Request failed
            raise InvalidRequestResponse(
                f"get_trello_json() request failed with status: {response.status_code}"
            )

        # get response json
        response_content = response.content
        dict = json.loads(response_content)

        return dict

    def get_board(self, board_id) -> dict:
        """Gets info about a Trello board

        Args:
            board_id (str): Trello board id e.g. 5e1fa572a76312xxxxxxxx

        Returns:
            dict: containing general board info
        """
        board_dict = self.get_trello_json(f"/1/boards/{board_id}")

        return board_dict

    def get_cards(self, board_id: str) -> dict:
        """Gets all cards belonging to a board

        Args:
            board_id (str): _description_

        Returns:
            dict: _description_
        """
        cards = self.get_trello_json(f"/1/boards/{board_id}/cards")

        return cards

    def get_card_detail(self, card_id: str) -> dict:
        """Gets card detail for a given card_id

        Args:
            card_id (str): _description_

        Returns:
            dict: _description_
        """
        card_detail = self.get_trello_json(f"/1/cards/{card_id}")

        return card_detail

    def get_created_date(self, id: str) -> datetime:
        """Gets the created date for a given board or card id
        The first 8 characters of the hexadecimal ID represent a Unix timestamp,
        which can then be translated into a date
        https://support.atlassian.com/trello/docs/getting-the-time-a-card-or-board-was-created/
        e.g. id_board = "4d5ea62fd76aaxxxxxxxx"
        card_id = "5e1fb5af9cc58xxxxxxxxxx"

        Args:
            id (str): a board_id or card_id

        Returns:
            datetime: datetime object e.g. '2020-01-16 12:00:31+00:00'
        """

        creation_time = datetime.fromtimestamp(int(id[0:8], 16))
        utc_creation_time = pytz.utc.localize(creation_time)

        return utc_creation_time


def main():
    print("***************************************")
    print("Jono's Trello scraper")
    print("")

    log_level = "INFO"
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    # load trello API from credentials file
    load_dotenv(TRELLO_CREDENTIALS_PATH)

    try:
        trello_api_key = Path(os.getenv("TRELLO_API_KEY"))
        trello_api_token = Path(os.getenv("TRELLO_API_TOKEN"))
        trello_board_id = Path(os.getenv("TRELLO_BOARD_ID"))
    except TypeError:
        raise InvalidCredentialsFile(
            "Could not load env file. Check TRELLO_CREDENTIALS_PATH is correct"
        )

    scraper = TrelloScraper(trello_api_key, trello_api_token)

    logging.info(f"Scraping data for BOARD_ID: {trello_board_id}")
    board = scraper.get_board(trello_board_id)
    board_name = board["name"]

    # get cards on board
    cards = scraper.get_cards(trello_board_id)
    num_cards = len(cards)

    logging.info(f"board_url: {board['url']}")
    logging.info(f"'{board_name}' contains {num_cards} card(s):")

    table = Table()
    table.add_column("number", style="magenta")
    table.add_column("card_name", style="green")
    table.add_column("created_date", style="green")
    table.add_column("dateLastActivity", style="green")
    table.add_column("URL", style="green")

    # loop over cards and extract details we want
    for card_key, card in enumerate(cards):
        card_id = card["id"]
        card_name = card["name"]
        url = card["url"]
        last_activity = card["dateLastActivity"]
        created_date = scraper.get_created_date(card_id)

        table.add_row(
            str(card_key + 1),
            str(card_name),
            str(created_date),
            str(last_activity),
            str(url),
        ),

    console.print(table)


if __name__ == "__main__":
    typer.run(main)
