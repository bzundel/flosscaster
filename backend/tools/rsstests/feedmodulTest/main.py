from datetime import datetime, timezone
from rss_feed_generator import RSSFeedGenerator
# Diese datei nur als beispiel wie ich den feed generator nutzen kann
def main():
    # Erstellen Sie eine Instanz des RSSFeedGenerator
    feed_generator = RSSFeedGenerator("Mein RSS Feed", "Dies ist eine Beschreibung meines RSS Feeds.")
    
    # Artikel hinzufügen
    feed_generator.add_item("Erster Artikel", "Dies ist die Beschreibung des ersten Artikels.", datetime.now(timezone.utc))
    feed_generator.add_item("Zweiter Artikel", "Dies ist die Beschreibung des zweiten Artikels.", datetime.now(timezone.utc))
    
    # RSS-Feed generieren
    feed_generator.generate_feed()

if __name__ == "__main__":
    main()

