import requests
import json

class Github():

    def __init__(self):
        self.conf = json.load(open('configuration.json'))
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': "Bearer " + self.conf['token'],
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.endpoint = self.conf['github_api'].format(self.conf['rep_owner'], self.conf['rep_name'])

    # returns a list of all the open issues in the repo
    def open_issues(self):
        response = requests.get(self.endpoint, headers=self.headers).json()
        open_issues = [issue for issue in response if issue['state'] == 'open']
        return open_issues

    # prints the issues from the repo which have the desired label
    def num_of_labeled_issues(self, targ_label: str):
        response = self.open_issues()
        labled_issues = [issue for issue in response if any(label.get('name') == targ_label for label in issue.get('labels', []))]
        print(len(labled_issues))

    # creates and validates the creation of an issue returns the creation response
    def create_issue(self, name: str, lang: str):
        body = {"title": f"{name}'s  issue",
                "body": f"This issue was created via REST API from {lang} by {name}",
                "assignees": ["topq-practice"],
                "labels": ["practice1"]}
        response = requests.post(self.endpoint, json.dumps(body), headers=self.headers)
        assert response.status_code == 201
        return response.json()

    # validates issue has been correctly added
    def test_issues_increament(self, initial_number_of_issues: int, new_issue: json):
        new_list_of_issues = git.open_issues()
        assert initial_number_of_issues + 1 == len(new_list_of_issues)
        assert json.dumps(new_issue, sort_keys=True), json.dumps(new_list_of_issues[0], sort_keys=True)

    # changes the state of an issue to close
    def close_issue(self, number: int):
        endpoint = self.endpoint + f'/{number}'
        body = {'state': 'closed', 'state_reason': 'not_planned'}
        response = requests.patch(endpoint,  json.dumps(body), headers=self.headers)
        assert response.status_code == 200

    # validates issue has been correctly closed
    def test_issue_eliminated(self, number: int):
        issues = self.open_issues()
        assert not any(issue['number'] == number for issue in issues)


if __name__ == '__main__':
    git = Github()

    # 1
    initial_issues = git.open_issues()
    initial_number_of_issues = len(initial_issues)
    print(initial_number_of_issues)

    # 2
    git.num_of_labeled_issues('practice1')

    # 3, 4
    created_issue = git.create_issue('Michael', 'python')
    first_new_issue_id = created_issue['number']

    # 5
    git.test_issues_increament(initial_number_of_issues, initial_issues[0])

    # 6
    git.close_issue(first_new_issue_id)

    # 7
    git.test_issue_eliminated(first_new_issue_id)
