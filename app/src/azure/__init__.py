from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Fill in with your personal access token and org URL
personal_access_token = 'ecjnirug35zewrestmclnailja2caz3iq3xyj4fe2dzuvoiu6vna'
organization_url = 'https://dev.azure.com/pdasolucoes'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()
git_client = connection.clients.get_git_client()
# Get the first page of projects
get_projects_response = core_client.get_projects()
print("get_projects_response",get_projects_response)
index = 0
while get_projects_response is not None:
    for project in get_projects_response.value:
        print("[" + str(index) + "] " + project.id + " > " + project.name)
        repos = git_client.get_repositories(project.id)
        print("repos",repos)
        index += 1
    if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
        # Get the next page of projects
        get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
    else:
        # All projects have been retrieved
        get_projects_response = None