import os
import argparse
import datetime
from lxml import etree

# Argumente definieren
parser = argparse.ArgumentParser(description='Füge eine neue Episode zu einem Podcast-RSS-Feed hinzu.')
parser.add_argument('title', type=str, help='Titel der neuen Episode')
parser.add_argument('url', type=str, help='URL zur neuen Episode')
parser.add_argument('description', type=str, help='Beschreibung der neuen Episode')

args = parser.parse_args()

# Verzeichnis und Dateiname
directory = './rss'  # Aktuelles Verzeichnis mit dem Unterordner 'rss'
filename = 'podcast.xml'  # Name der RSS-Datei

# Vollständiger Pfad zur Datei
file_path = os.path.join(directory, filename)

# RSS-Feed laden
with open(file_path, 'rb') as f:
    feed_content = f.read()

# XML-Parser initialisieren
root = etree.fromstring(feed_content)

# Neue Episode hinzufügen
new_episode_title = args.title
new_episode_url = args.url
new_episode_description = args.description
new_episode_pubDate = str(datetime.datetime.now())

# Erstelle ein neues Item
new_item = etree.Element('item')
etree.SubElement(new_item, 'title').text = new_episode_title
etree.SubElement(new_item, 'description').text = new_episode_description
etree.SubElement(new_item, 'pubDate').text = new_episode_pubDate
enclosure = etree.SubElement(new_item, 'enclosure')
enclosure.set('url', new_episode_url)
enclosure.set('type', 'audio/flac')

# Füge das neue Item zum Channel hinzu
channel = root.find('channel')
channel.append(new_item)

# Speichern des aktualisierten Feeds
with open(file_path, 'wb') as f:
    f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

print(f'Die neue Episode "{new_episode_title}" wurde erfolgreich zu {filename} hinzugefügt.')
