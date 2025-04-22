from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup

# Pfad zur HTML-Datei
html_file_path = 'hello.html'  # Ersetze dies durch den Pfad zu deiner HTML-Datei

# Lese den HTML-Inhalt aus der Datei
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse den HTML-Inhalt mit BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Finde die Liste (ul) und die Listeneinträge (li)
list_items = soup.find('ul').find_all('li')

# Erstelle einen FeedGenerator
fg = FeedGenerator()
fg.id('http://example.com/rss')  # Setze die ID des Feeds
fg.title('Meine Liste')            # Setze den Titel des Feeds
fg.link(href='http://example.com', rel='alternate')  # Setze den Link zur Website
fg.description('Dies ist ein RSS-Feed für meine Liste.')  # Setze die Beschreibung

# Füge Einträge hinzu
for item in list_items:
    fe = fg.add_entry()
    fe.id(f'http://example.com/item/{item.text}')  # Setze die ID des Eintrags
    fe.title(item.text)                             # Setze den Titel des Eintrags
    fe.link(href=f'http://example.com/item/{item.text}')  # Setze den Link zum Eintrag
    fe.description(f'Dies ist der Eintrag für {item.text}.')  # Setze die Beschreibung des Eintrags

# Generiere den RSS-Feed
rss_feed = fg.rss_str(pretty=True)  # Generiere den RSS-Feed als String

# Speichere den RSS-Feed in einer Datei
with open('feed.xml', 'wb') as feed_file:
    feed_file.write(rss_feed)

print("RSS-Feed wurde erfolgreich generiert und in 'feed.xml' gespeichert.")

