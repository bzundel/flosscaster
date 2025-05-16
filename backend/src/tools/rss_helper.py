import os
import argparse
import datetime
from lxml import etree

RSS_FILE = os.getenv("RSS_FILE") # fetch target rss file from env var. must be given as relative path (./test.rss instead of test.rss)

def add_episode_to_podcast(title: str, url: str, description: str):
    if not os.path.exists(os.path.dirname(RSS_FILE)):
        os.makedirs(os.path.dirname(RSS_FILE), exist_ok = True) # create file path if it doesn't exist

    if not os.path.isfile(RSS_FILE):
        pass # TODO create basic rss feed from template

    with open(RSS_FILE, 'rb') as f:
        feed_content = f.read()

    # XML-Parser initialisieren
    root = etree.fromstring(feed_content)

    # Neue Episode hinzufügen
    new_episode_pubDate = str(datetime.datetime.now())

    # Erstelle ein neues Item
    new_item = etree.Element('item')
    etree.SubElement(new_item, 'title').text = title
    etree.SubElement(new_item, 'description').text = description
    etree.SubElement(new_item, 'pubDate').text = new_episode_pubDate
    enclosure = etree.SubElement(new_item, 'enclosure')
    enclosure.set('url', url)
    enclosure.set('type', 'audio/mp3')

    # Füge das neue Item zum Channel hinzu
    channel = root.find('channel')
    channel.append(new_item)

    # Speichern des aktualisierten Feeds mit Zeilenumbrüchen und Einrückungen
    with open(RSS_FILE, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
