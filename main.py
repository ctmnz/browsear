import argparse
import re
import sys
import newspaper
from gtts import gTTS
from pygame import mixer
import pygame

ARTICLE_MP3_FILE = './article_read.mp3'


def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

url_parser = argparse.ArgumentParser(description='Parse the url address of the article')
url_parser.add_argument('--url', help='Provide an URL address for the article that you want to listen to.', required=True)
args = url_parser.parse_args()

# print("url = {}".format(args.url))

if not check_url(args.url):
    print("\n\n\nWARNING: The provided url address is not valid. It should look lie the following example example: https://your.address.com/article.html ")
    url_parser.print_help()
    exit(1)

article = newspaper.Article(args.url)
article.download()
article.parse()

tts = gTTS(article.text, lang="en")
tts.save(ARTICLE_MP3_FILE)

mixer.init()
mixer.music.load(ARTICLE_MP3_FILE)
mixer.music.play()

while mixer.music.get_busy():
    pygame.time.wait(100)
print("Finished")

