import requests
import json

conf = json.load(open('configuration.json'))

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': "Bearer " + conf['token'],
    'X-GitHub-Api-Version': '2022-11-28'
}
endpoint = 'https://api.github.com/repos/{}/{}/issues'.format(conf['rep_owner'], conf['rep_name'])

def num_of_open_issues():
    response = requests.get(endpoint, headers=headers).json()
    open_issues = [issue for issue in response if issue['state'] == 'open']
    print(len(open_issues))

def num_of_labeled_issues(targ_label: str):
    response = requests.get(endpoint, headers=headers).json()
    labled_issues = [issue for issue in response if any(label.get('name') == targ_label for label in issue.get('labels', []))]
    print(len(labled_issues))

def create_issue(name:str , lang: str):
    body = {"title":f"{name}'s  issue",
            "body":f"This issue was created via REST API from {lang} by {name}",
            "assignees":["topq-practice"],
            "labels":["practice1"]}
    response = requests.post(endpoint, json.dumps(body), headers=headers).json()
    #todo: perhaps asserting the creation here is needed.


if __name__ == '__main__':
    num_of_open_issues()
    num_of_labeled_issues('practice1')
    # create_issue('Michael', 'python')
