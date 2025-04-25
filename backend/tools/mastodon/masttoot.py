import argparse
from mastodon import Mastodon

# Definiere den Access Token hier
ACCESS_TOKEN = 'your_access_token_here'  # Ersetze dies durch deinen tatsächlichen Access Token

def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description='Post a Toot on Mastodon.')
    parser.add_argument('message', type=str, help='The message to post as a Toot')

    args = parser.parse_args()

    # Mastodon-Instanz erstellen
    mastodon = Mastodon(access_token=ACCESS_TOKEN)

    # Toot erstellen
    mastodon.toot(args.message)
    print("Successfully posted Toot:", args.message)

if __name__ == "__main__":
    main()

