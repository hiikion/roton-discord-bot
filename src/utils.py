import requests
import json
import pyshorteners

def random_animal(animal):
    response = requests.get('https://some-random-api.ml/img/' + animal)
    if 300 > response.status_code >= 200:
        json_data = json.loads(response.text)
        data = json_data['link']
    else:
        data = 'host not responding or invalid animal'

    return data

def random_anime_quote():
    response = requests.get('https://some-random-api.ml/animu/quote')
    if 300 > response.status_code >= 200:
        json_data = json.loads(response.text)
        data = {'sentence': json_data['sentence'], 'characther': json_data['characther'], 'anime': json_data['anime']}
    else:
        data = 'error while getting the quoute'
    
    return data

def r_anime(category):
    response = requests.get('https://api.waifu.pics/sfw/' + category)
    if 300 > response.status_code >= 200:
        json_data = json.loads(response.text)
        data = json_data['url']
    else:
        data = 'host not responding or invalid category'

    return data

def shorten_url(link):
    if 'http://' or 'https://' in link and '.' in link:
        s = pyshorteners.Shortener()
        shorted = s.isgd.short(link)
        return shorted
    else:
        return 'invalid url format'

def get_insult(lang):
    response = requests.get('https://evilinsult.com/generate_insult.php?lang='+ lang +'&type=json')
    if 300 > response.status_code >= 200:
        json_data = json.loads(response.text)
        data = json_data['insult']
    else:
        data = 'host not responding or invalid lang'

    return data