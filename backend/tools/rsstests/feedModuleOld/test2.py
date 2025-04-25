import requests
from feedgen.feed import FeedGenerator
import time

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

def save_rss_to_file(feed):
    """Save the RSS feed to a file."""
    with open("rss_feed.xml", "w") as f:
        f.write(feed)
    print("RSS feed saved to rss_feed.xml")

def post_rss_to_server():
    """Post the RSS feed to the server."""
    with open("rss_feed.xml", "r") as f:
        rss_content = f.read()
    
    response = requests.post(f"{SERVER_URL}/api/create", data=rss_content, headers={'Content-Type': 'application/xml'})
    if response.status_code == 200:
        print("Successfully posted RSS feed to the server.")
    else:
        print(f"Error posting RSS feed: {response.status_code}, {response.text}")
'''
def main():
    # Hier podcast einsetzen
    # RSS-Feed erstellen
    rss_feed = create_rss_feed(podcasts)
    
    # RSS-Feed in eine Datei speichern
    save_rss_to_file(rss_feed)
    
    # RSS-Feed an den Server senden
    post_rss_to_server()

if __name__ == "__main__":
    main()
'''
