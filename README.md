# trello-api-scraper
Uses the [Trello API](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) to get board and card data in json format.

This script gets the number of cards for a particular Trello board and uses CURL 
requests to pull data using the Trello API. See:

https://stateful.com/blog/trello-api-examples

Tested under Ubuntu 20.04.

## Installation

1) Clone this repo to your local machine.

2) Install [Python Poetry](https://python-poetry.org/)

3) Install script dependancies with:
```
sudo poetry install
```

4) To automate this script with a CRON job, it's advised to store your Trello API creds
in a secure folder e.g. `/root/trello_credentials` containing the following variables:
```
TRELLO_API_KEY=xxxxxxxxxxxx
TRELLO_API_TOKEN=xxxxxxxxxxxx
TRELLO_BOARD_ID=xxxxxxxxxxxx
```
Your Trello board id can be found by putting `.json` at end of the Trello board URL
in your browser e.g.

https://trello.com/b/xxxxxxxx/your-board-name.json

## Usage
Run this script as root/sudo user so the script can pull in the trello_credentials correctly.
e.g.
```
sudo poetry run python get_trello_cards.py
```
