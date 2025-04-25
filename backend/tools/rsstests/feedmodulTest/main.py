from datetime import datetime, timezone
from rss_feed_generator import RSSFeedGenerator
#Beispiel wie das Module verwendet weren kann
# Erstelle eine Instanz des RSSFeedGenerator
rss_generator = RSSFeedGenerator("Mein RSS-Feed","Dies ist ein Beispiel für einen RSS-Feed.")

# Füge einen Artikel mit Enclosure hinzu
rss_generator.add_item(
    title='dreisiben Artikel',
    description='das ist n test17 .',
    date = datetime.now(timezone.utc),  # Beispiel-Datum
    enclosure_url='http://example.com/audio24.flac',  # Beispiel-URL
    enclosure_type='audio/flac',  # Typ der Enclosure
    enclosure_length=338  # Größe der Datei in Bytes
)

# Generiere den RSS-Feed und speichere ihn in einer Datei
rss_generator.generate_feed()

