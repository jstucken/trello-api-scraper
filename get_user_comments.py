# This script uses Trello API to get all comments made by a Trello user on a specific
# board, and saves them to a JSON file. Comments will be listed in descending order by
# date. Requires dotenv Python module to be installed (pip install python-dotenv)

import requests
import json
from dotenv import load_dotenv
import os

# Prompt user for credentials if not set in env variables
# username and board_id can be obtained by opening your Trello board in your browser
# and appending .json to the end of the URL.
# Then search for 'username' and 'id' (aka board_id) in the JSON response.
api_key = os.getenv("TRELLO_API_KEY")
token = os.getenv("TRELLO_API_TOKEN")
board_id = os.getenv("TRELLO_BOARD_ID")

if not api_key:
    api_key = input("Enter Trello API key: ")

if not token:
    token = input("Enter Trello token: ")

if not board_id:
    board_id = input("Enter Trello board_id: ")

username = input("Enter Trello username (e.g. john_smith): ")
url = f"https://api.trello.com/1/members/{username}/actions"

params = {
   "filter": "commentCard",
   "memberCreator": "true",
   "memberCreator_fields": "username",
   "board": "true",
   "board_fields": "name",
    "idBoard": board_id,
    "limit": 1000,
    "key": api_key,
    "token": token
}

all_comments = []

# Get batches of 1000 comments (the max allowed at once by the API), then bundle them
# all together
while True:
    response = requests.get(url, params=params)
    comments = response.json()
    all_comments.extend(comments)
    if len(comments) < 1000:
        break
    oldest_comment = comments[-1]["date"]
    params["before"] = oldest_comment

num_comments = len(all_comments)
print(f"{num_comments} Trello comments found for {username} on board_id: {board_id}")

filename = f"{username}_comments_{num_comments}.json"
with open(filename, "w") as f:
    f.write(json.dumps(all_comments))

print(f"Saved JSON file: {filename}")
print("Done")