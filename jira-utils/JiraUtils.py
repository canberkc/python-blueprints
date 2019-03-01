from jira import JIRA

server = ""
user = ""
password = ""


jira_server = {'server': server}
jira = JIRA(options=jira_server, basic_auth=(user, password))


issue = jira.issue('issue-id')
print(issue.fields.summary)
