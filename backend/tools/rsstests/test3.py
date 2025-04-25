import argparse
import requests
from feedgen.feed import FeedGenerator

SERVER_URL = "http://localhost:5000"  # URL des laufenden Flask-Servers

class Podcast:
    def __init__(self, id, title, description, date):
        self.id = id
        self.title = title
        self.description = description
        self.date = date

def create_rss_feed(podcasts):
    """Generate an RSS feed from a list of Podcast objects."""
    fg = FeedGenerator()
    fg.id('http://example.com/podcasts')
    fg.title('Podcast Feed')
    fg.link(href='http://example.com/podcasts', rel='self')
    fg.description('A feed of all podcasts')

    for podcast in podcasts:
        fe = fg.add_entry()
        fe.id(f"http://example.com/podcasts/{podcast.id}")
        fe.title(podcast.title)
        fe.description(podcast.description)
        fe.pubDate(podcast.date)

    return fg.rss_str(pretty=True)

def post_rss_to_server(rss_feed):
    """Post the RSS feed to the server."""
    response = requests.post(f"{SERVER_URL}/api/create", data=rss_feed, headers={'Content-Type': 'application/xml'})
    if response.status_code == 200:
        print("Successfully posted RSS feed to the server.")
    else:
        print(f"Error posting RSS feed: {response.status_code}, {response.text}")

def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description='Create a podcast RSS feed and post it to the server.')
    parser.add_argument('id', type=int, help='The ID of the podcast')
    parser.add_argument('title', type=str, help='The title of the podcast')
    parser.add_argument('description', type=str, help='The description of the podcast')
    parser.add_argument('date', type=str, help='The publication date of the podcast (ISO format)')

    args = parser.parse_args()

    # Podcast-Objekt erstellen
    podcast = Podcast(args.id, args.title, args.description, args.date)

    # RSS-Feed erstellen
    rss_feed = create_rss_feed([podcast])
    
    # RSS-Feed an den Server senden
    post_rss_to_server(rss_feed)

if __name__ == "__main__":
    main()

