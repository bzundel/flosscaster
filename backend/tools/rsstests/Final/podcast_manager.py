import FeedEditorModule
import os
import argparse
import datetime
from lxml import etree

def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description='Füge eine neue Episode zu einem Podcast hinzu.')
    parser.add_argument('title', type=str, help='Der Titel der Episode')
    parser.add_argument('url', type=str, help='Die URL der Episode (z.B. Audio-Datei)')
    parser.add_argument('description', type=str, help='Die Beschreibung der Episode')

    args = parser.parse_args()

    # Füge die Episode zum Podcast hinzu
    FeedEditorModule.add_episode_to_podcast(args.title, args.url, args.description)

if __name__ == '__main__':
    main()

