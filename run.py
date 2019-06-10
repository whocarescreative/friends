
# Import libraries
import requests
import urllib.request
import time
import re
import json

import html2text

from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://fangj.github.io/friends/season/0110.html'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

# print(soup.prettify())


# file2 = open("dump.txt","w+") 
# text = html2text.html2text(response.text)
# file2.write(text)

data = {
    'seasons':[]
}

lines = []

for p in soup.find_all('p'):
    actionPattern = '\([^)]*\)'
    cleanLine = re.sub(actionPattern, "", p.getText())
    b = p.find('b')
    if b is not None:
        b_text = b.get_text()
        # print(b_text)

        utterance = cleanLine.split(b_text,1)[1].strip()
        actor = b_text.replace(":"," ").strip()

        line = {
            'actor': actor,
            'text': utterance
        }
        lines.append(line)

with open('season1.json', 'w') as out:
    datadump = {
        "data": lines
    }
    json.dump(datadump, out)
   



# with open("dump.txt")  as f:
#     for line in f:
#         if line.strip():
#             actionPattern = '.*?\((.*?)\)'
#             action = re.findall(actionPattern, line)

#             test = re.sub(actionPattern, "", line)
#             print(test)

#             # if (len(action) > 0):
#             #     print(action)

#             namePattern = '\*{2}(.*):\*{2}'
#             name = re.findall(namePattern, line)

#             # namePattern = line.split("**",1)[1] 
            # text = 
