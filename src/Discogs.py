import time
from env import *
import style

import requests
import json

import mutagen
from mutagen.mp3 import MP3

def sleep():
    prefix = 'discogs api call: '
    print(prefix + style.yellow('sleeping...'))
    time.sleep(60 / ENV_DISCOGS_MAX_RATE)
    print(prefix + style.yellow('go!') + '\n')

def getReleaseFromMaster(master_id):
    sleep()

    base_url = 'https://api.discogs.com/masters/'
    response = requests.get(base_url + master_id)
    response_json = json.loads(response.text)
    
    release_id = response_json['main_release_url'].rsplit('/', 1)[1]

    return release_id

def Discogs(files):
    # get json
    base_url = 'https://api.discogs.com/releases/'
    file_extension = files[0].rsplit('.', 1)[1]

    # logics by extensions
    # FLAC
    if file_extension == 'flac':
        file = mutagen.File(files[0])

        if file.get('custom') is None:
            return None

        if file.get('custom')[0][:4] == ENV_TAGGING_DONE:
            return ENV_TAGGING_DONE
        
        if file.get('custom')[0][:4] == ENV_TAGGING_TODO:
            return ENV_TAGGING_TODO
        
        url = file.get('custom')[0]
        id = url.rsplit('/', 1)[1]

    # MP3
    elif file_extension == 'mp3':
        file = MP3(files[0])

        if file.get('TXXX:Custom') is None:
            return None
        
        if str(file.get('TXXX:Custom'))[:4] == ENV_TAGGING_DONE:
            return ENV_TAGGING_DONE
        
        if str(file.get('TXXX:Custom'))[:4] == ENV_TAGGING_TODO:
            return ENV_TAGGING_TODO
        
        url = str(file.get('TXXX:Custom'))
        id = url.rsplit('/', 1)[1]

    # logics if discogs/master
    if '/master/' in url:
        id = getReleaseFromMaster(id)

    sleep()
    
    response = requests.get(base_url + id)
    
    return {
        'json': json.loads(response.text),
        'url': base_url + id,
    }