# trello-api-scraper
Uses Trello API to get board and card data in json format.

This script gets the number of cards for a particular Trello board and uses CURL 
requests to pull data using the Trello API.
see https://stateful.com/blog/trello-api-examples
https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/

To automate this script with a CRON job, it's advised to store your Trello API creds
in a secure folder e.g. `/root/trello_credentials` containing the following variables:
```
TRELLO_API_KEY=xxxxxxxxxxxx
TRELLO_API_TOKEN=xxxxxxxxxxxx
TRELLO_BOARD_ID=xxxxxxxxxxxx
```
Your Trello board id can be found by putting `.json` at end of the Trello board URL
in your browser.

Then run this script as root/sudo user so the script can pull in the trello_credentials correctly.
e.g.
```sudo poetry run python get_trello_cards.py```