import os
import argparse
import datetime
import pytz
from lxml import etree

def add_episode_to_podcast(title: str, url: str, description: str):
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
    new_episode_pubDate = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%a, %d %b %Y %H:%M:%S %z')

    # Erstelle ein neues Item
    new_item = etree.Element('item')
    etree.SubElement(new_item, 'title').text = title
    etree.SubElement(new_item, 'description').text = description
    etree.SubElement(new_item, 'pubDate').text = new_episode_pubDate
    enclosure = etree.SubElement(new_item, 'enclosure')
    enclosure.set('url', url)
    enclosure.set('type', 'audio/mpeg')

    # Füge das neue Item zum Channel hinzu
    channel = root.find('channel')
    channel.append(new_item)
    
    # Aktualisiere lastBuildDate
    last_build_date = channel.find('lastBuildDate')
    last_build_date.text = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%a, %d %b %Y %H:%M:%S %z')

    # Speichern des aktualisierten Feeds mit Zeilenumbrüchen und Einrückungen
    with open(file_path, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    print(f'Die neue Episode "{title}" wurde erfolgreich zu {filename} hinzugefügt.')

