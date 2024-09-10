import os

from jira import JIRA

jira_server = os.environ['JIRA_SERVER']
user = os.environ['JIRA_USER']
api_token = os.environ['API_TOKEN']


def setup_jira() -> JIRA:
    authed_jira = JIRA(basic_auth=(user, api_token), server=jira_server)

    return authed_jira


def list_project(auth_jira: JIRA):
    projects = auth_jira.projects()
    for project in projects:
        print('ID: {0} Key: {1} Name: {2}'.format(project.id, project.key, project.name))


def get_active_sprints_for_project(auth_jira: JIRA, project_key: str):
    boards = auth_jira.boards(name=project_key)
    active_sprint = None
    for board in boards:
        sprints = jira.sprints(board.id)
        print(f"Sprints for board {board.name}:")
        for sprint in sprints:
            print(f" - {sprint.name} (ID: {sprint.id}, State: {sprint.state})")
            if sprint.state == 'active':
                active_sprint = sprint

    return active_sprint


def list_sprint_issues(auth_jira: JIRA, project_id: str, sprint_id: str):
    issues = auth_jira.search_issues('project={0} and sprint = {1}'.format(project_id, sprint_id))
    for issue in issues:
        print(issue)


if __name__ == "__main__":
    jira = setup_jira()
    # list_project(jira)
    active_sprint = get_active_sprints_for_project(jira, 'DED')
    print(active_sprint.id)
    list_sprint_issues(jira, '10051', active_sprint.id)
