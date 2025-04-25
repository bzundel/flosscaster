import os
import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime

class RSSFeedGenerator:
    def __init__(self, feed_title, feed_description):
        self.feed_title = feed_title
        self.feed_description = feed_description
        self.items = []
        self.rss_dir = 'rss'
        
        # Verzeichnis erstellen, falls es nicht existiert
        if not os.path.exists(self.rss_dir):
            os.makedirs(self.rss_dir)

    def add_item(self, title, description, date, enclosure_url=None, enclosure_type=None, enclosure_length=None):
        """Fügt einen neuen Artikel zum Feed hinzu."""
        item = {
            'title': title,
            'description': description,
            'date': date,
            'enclosure_url': enclosure_url,
            'enclosure_type': enclosure_type,
            'enclosure_length': enclosure_length
        }
        self.items.append(item)

    def generate_feed(self):
        """Generiert den RSS-Feed und speichert ihn in einer Datei."""
        fg = FeedGenerator()
        fg.id('http://example.com')  # Setzen Sie die ID des Feeds
        fg.title(self.feed_title)
        fg.description(self.feed_description)
        fg.link(href='http://example.com', rel='self')

        for item in self.items:
            fe = fg.add_entry()
            fe.title(item['title'])
            fe.description(item['description'])
            fe.pubDate(item['date'])

            # Füge die Enclosure-Informationen hinzu, falls vorhanden
            if item['enclosure_url']:
                fe.enclosure(item['enclosure_url'], item['enclosure_length'], item['enclosure_type'])

        # RSS-Feed in einer Datei speichern
        feed_file_path = os.path.join(self.rss_dir, 'feed.xml')
        fg.rss_file(feed_file_path)

        print(f"RSS-Feed wurde erfolgreich in '{feed_file_path}' gespeichert.")
