
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
episode_count = 0

episodes = []
seasons = []

season_num = 0
episode_num = 0


def season2Check(speaker):
    if speaker == 'RUSS':
        speaker = 'Ross'

    if speaker == 'MNCA':
        speaker = 'Monica'
        
    if speaker == 'CHAN':
        speaker = 'Chandler'

    if speaker == 'RACH':
        speaker = 'Rachel'

    if speaker == 'JOEY':
        speaker.capitalize()
    
    if speaker == 'PHOE':
        speaker = 'Phoebe'
    return speaker



def massageLine(line):

    speaker = None
    utterance = None

    actionPattern = "[\(\[].*?[\)\]]"
    cleanLine = re.sub(actionPattern, "", line)

    # print(cleanLine)

    if ':' in cleanLine:
        speaker = cleanLine.split(':',1)[0].strip()
        speaker = speaker.lower()

        if not speaker.endswith(" by") and not "commercial voiceover" in speaker:
            utterance = cleanLine.split(':',1)[1].strip()
            speaker = speaker.replace(":"," ").strip()

            if int(season_num) is 2:
                speaker = season2Check(speaker)

            return {
                'speaker': speaker,
                'text': utterance
            }

    return None


def run():

    global episode_count
    global season_num
    global episode_num

    url = None
    if (season_num == 9 and episode_num == 23):
        url = 'https://fangj.github.io/friends/season/0923-0924.html'
    elif (season_num == 10 and episode_num == 17):
        url = 'https://fangj.github.io/friends/season/1017-1018.html'
    elif (season_num == 6 and episode_num == 15):
        url = 'https://fangj.github.io/friends/season/0615-0616.html'
    elif (season_num == 2 and episode_num == 12):
        url = 'https://fangj.github.io/friends/season/0212-0213.html'
    else:
        url = baseUrl+ f'{str(season_num).zfill(2)}{str(episode_num).zfill(2)}.html'
   
    response = requests.get(url)

    
    if response.status_code == 200:
        print(url)
        html = response.text

        text_maker = html2text.HTML2Text()
        text_maker.ignore_emphasis = True

        text = text_maker.handle(html)

        if season_num == 2 and episode_num >= 12:
            formatted_text = text.replace('  ','').replace('\n\n','**').replace('\n',' ').replace('**','\n')
        else:
            formatted_text = text.replace('\n\n','**').replace('\n',' ').replace('**','\n')


        episode_count = episode_count + 1
        episode_lines = []

        file1 = open("myfile.txt","w")#write mode 
        file1.write(formatted_text) 
        file1.close() 

        with open("myfile.txt") as fp:  
            line = fp.readline()

            while line:
                if (line == '\n'):
                    print('********')
                else:
                    line_obj = massageLine(line)
                    if (line_obj is not None):
                        episode_lines.append(line_obj)

                line = fp.readline()


        episode = {
            'num':episode_count,
            'lines':episode_lines
        }

        episodes.append(episode)


for i in range (2,3):
    season_num = i
    episodes = []

    for j in range(10, 27):
        episode_num = j 
        run()

    season = {
        'num': season_num,
        'episodes':episodes
    }
    seasons.append(season)
    with open(f'data{season_num}.json', 'w') as out:
        datadump = {
            "data": season
        }
        json.dump(datadump, out)
    
