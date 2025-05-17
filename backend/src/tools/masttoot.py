import os
import sys
from mastodon import Mastodon

def masttoot(title: str, url: str, description: str):
    """Publishes a new toot using the input, also sends a reply to the announcement with the description."""

    post_text = "The Flosscasters have released a new podcast episode: " + title + ". Check it out @ " + url

    #Mastodon-Instanz
    mastodon = Mastodon(
        client_id = os.getenv("MASTODON_CLIENT_KEY"),
        client_secret = os.getenv("MASTODON_CLIENT_SECRET"),
        access_token = os.getenv("MASTODON_ACCESS_TOKEN"),
        api_base_url = os.getenv("MASTODON_BASE_URL")
    )

    #Publish the toot and reply to it with the description
    to_reply = mastodon.status_post(post_text)
    mastodon.status_post(description, in_reply_to_id=to_reply.id)

if __name__ == "__main__":
    masttoot(sys.argv[1], sys.argv[2], sys.argv[3])

