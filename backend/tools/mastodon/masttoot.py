import argparse
import os
import sys
import time

from mastodon import Mastodon
from dotenv import load_dotenv
import feedparser

def masttoot(title: str, url: str, description: str):
    """Publishes a new toot using the input, also sends a reply to the announcement with the description."""

    #Load access information from .env file and create the initial announcement text
    load_dotenv()
    post_text = "The Flosscasters have released a new Podcast Episode: " + title + "Check it out @ " + url

    #Mastodon-Instanz
    mastodon = Mastodon(
        client_id=os.getenv("CLIENT_KEY"),
        client_secret=os.getenv("CLIENT_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url="https://mastodon.social/"
    )

    #Create a list of current toots
    toot_so_far = []
    for posts in mastodon.account_statuses(os.getenv("ID")):
        toot_so_far.append(posts.id)

    #Publish the toot and waits 10s
    mastodon.status_post(post_text)
    time.sleep(10)

    #Checks for a new toot on the account and replies with the description of the episode
    for posts in mastodon.account_statuses(os.getenv("ID")):
        if posts.id not in toot_so_far:
            toot_so_far.append(posts.id)
            mastodon.status_post(description,in_reply_to_id=posts.id)

if __name__ == "__main__":
    masttoot(sys.argv[1], sys.argv[2], sys.argv[3])

