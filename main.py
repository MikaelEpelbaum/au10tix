import requests
import json

conf = json.load(open('configuration.json'))

# endpoint = 'https://github.com/{}/{}/issues'.format(conf['rep_owner'], conf['rep_name'])
endpoint = 'https://api.github.com/repos/topq-practice/api-practice/issues'


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': "Bearer " + conf['token'],
    'X-GitHub-Api-Version': '2022-11-28'
}

x = requests.request('GET', endpoint, headers=headers).json()

print(x)