import requests
from datetime import datetime
from tkinter import *

USERNAME = "WRITE AN USERNAME"
TOKEN = "WRITE UP ANY MADE UP TOKEN ID OF AT LEAST 18 CHARACTERS"
GRAPH_ID = "WRITE A GRAPH ID"
YELLOW = "#f7f5dd"
RED = "#e7305b"
GREEN = "#9bdeac"
FONT_NAME = "Courier"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"


# USER CREATION
def user_creation():
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
    print(response.text)


# GRAPH CREATION
def graph_creation():
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

    graph_config = {
        "id": GRAPH_ID,
        "name": "Coding Graph",
        "unit": "hour",
        "type": "float",
        "color": "sora"
    }

    headers = {
        "X-USER-TOKEN": TOKEN
    }

    response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
    print(response.text)

    print(f"Your pixel endpoint is {graph_endpoint}/{GRAPH_ID}.html")


def main():
    user_creation()
    graph_creation()


main()
