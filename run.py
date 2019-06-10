
# Import libraries
import requests
import urllib.request
import time
import re
import json

import html2text

from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
baseUrl = 'https://fangj.github.io/friends/season/'

soup = None



def extractLines():
    for p in soup.find_all('p'):
        actionPattern = '\([^)]*\)'
        cleanLine = re.sub(actionPattern, "", p.getText())
        b = p.find('b')
        if b is not None:
            b_text = b.get_text()

            if ':' in b_text:

                utterance = cleanLine.split(':',1)[1].strip()
                actor = b_text.replace(":"," ").strip()

                line = {
                    'actor': actor,
                    'text': utterance
                }
                lines.append(line)


lines = []

episodes = []

season = '02'
for i in range(1, 25):
    url = baseUrl+ f'{season}{str(i).zfill(2)}.html'

    print(url)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lines = []
    extractLines()

    episode = {
        'num':i,
        'lines':lines
    }

    episodes.append(episode)

with open(f'data{season}.json', 'w') as out:
    datadump = {
        "data": {
            'seasons': {
                'num':1,
                'episdodes': episodes
            }
        }
    }
    json.dump(datadump, out)
   


