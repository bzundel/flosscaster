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
    post_text = "The Flosscasters have released a new Podcast Episode: " + title + ". Check it out @ " + url

    #Mastodon-Instanz
    mastodon = Mastodon(
        client_id=os.getenv("CLIENT_KEY"),
        client_secret=os.getenv("CLIENT_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url="https://mastodon.social/"
    )

    #Publish the toot and reply to it with the description
    to_reply = mastodon.status_post(post_text)
    mastodon.status_post(description, in_reply_to_id=to_reply.id)

if __name__ == "__main__":
    masttoot(sys.argv[1], sys.argv[2], sys.argv[3])

