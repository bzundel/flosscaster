import os
import argparse
import datetime
import pytz
from lxml import etree

RSS_FILE = os.getenv("RSS_FILE") # fetch target rss file from env var. must be given as relative path (./test.rss instead of test.rss)

# Datum im format ISO 8601

RSS_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<rss version="2.0">
  <channel>
    <title>6 Sekunden podcast</title>
    <link>https://example.com/podcast</link>
    <description>Dies ist ein Beispiel-Podcast.</description>
    <language>de</language>
    <pubDate>Sun, 01 Jan 2023 00:00:00 +0100</pubDate>
    <lastBuildDate>2025-05-18 10:36:56.310687</lastBuildDate>
  </channel>
</rss>
"""

def add_episode_to_podcast(title: str, url: str, description: str):
    if not os.path.exists(os.path.dirname(RSS_FILE)):
        os.makedirs(os.path.dirname(RSS_FILE), exist_ok = True) # create file path if it doesn't exist

    if not os.path.isfile(RSS_FILE):
        with open(RSS_FILE, "w") as f:
            f.write(RSS_TEMPLATE) # create rss boilerplate of no feed exists

    with open(RSS_FILE, 'rb') as f:
        feed_content = f.read()

    # XML-Parser initialisieren
    root = etree.fromstring(feed_content)

    # Neue Episode hinzufügen
    new_episode_pub_date = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%a, %d %b %Y %H:%M:%S %z')

    # Erstelle ein neues Item
    new_item = etree.Element('item')
    etree.SubElement(new_item, 'title').text = title
    etree.SubElement(new_item, 'description').text = description
    etree.SubElement(new_item, 'pubDate').text = new_episode_pub_date
    enclosure = etree.SubElement(new_item, 'enclosure')
    enclosure.set('url', url)
    enclosure.set('length', str(os.path.getsize(os.path.join(os.environ['UPLOAD_PATH'], os.path.basename(url)))))
    enclosure.set('type', 'audio/mpeg')

    # Füge das neue Item zum Channel hinzu
    channel = root.find('channel')
    channel.append(new_item)
    
    # Aktualisiere lastBuildDate
    last_build_date = channel.find('lastBuildDate')
    last_build_date.text = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%a, %d %b %Y %H:%M:%S %z')

    # Speichern des aktualisierten Feeds mit Zeilenumbrüchen und Einrückungen
    with open(RSS_FILE, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
