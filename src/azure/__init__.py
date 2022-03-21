from azure.devops.connection import Connection
from azure.devops.v5_1.git.models import GitRepository, TeamProjectReference
from azure.devops.v5_1.work_item_tracking.models import Wiql,WorkItemReference,WorkItemQueryResult
from msrest.authentication import BasicAuthentication


class Azure:
    def __init__(self,personal_access_token:str, organization:str, default_project:str = None):
        self.__init__ = self
        self.personal_access_token = personal_access_token
        self.organization = organization
        self.organization_url = f"https://dev.azure.com/{self.organization}"
        self.default_project = default_project
        self.credentials = BasicAuthentication('', personal_access_token)
        self.__connection = Connection(base_url=self.organization_url, creds=self.credentials)
        self.__core_client = self.__connection.clients.get_core_client()
        self.__git_client = self.__connection.clients.get_git_client()
        self.__work_item_tracking_client = self.__connection.clients.get_work_item_tracking_client()
        self.projects = self.get_projects()

    def get_projects(self):
        get_projects_response = self.__core_client.get_projects()
        projetos = []
        index = 0
        while get_projects_response is not None:
            for project in get_projects_response.value:
                projetos.append(project)
                index += 1
            if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
                # Get the next page of projects
                get_projects_response = self.__core_client.get_projects(continuation_token=get_projects_response.continuation_token)
            else:
                # All projects have been retrieved
                get_projects_response = None
        return projetos
    def get_repositories(self,project_id: str = None):
        if project_id is not None:
            repos = self.__git_client.get_repositories(project_id)
            return repos
        if self.default_project is not None:
            repos = self.__git_client.get_repositories(self.default_project)
            print("repos",repos[0])
            return repos
        raise Exception('Project ID not informed')
    def get_tasks(self):
        bugs = Wiql(
            query="""
                select [System.Id],
                    [System.WorkItemType],
                    [System.Title],
                    [System.State],
                    [System.AreaPath],
                    [System.IterationPath],
                    [System.Tags]
                from WorkItems
                where [System.WorkItemType] = 'Bug'
                order by [System.ChangedDate] desc"""
            )
        work_items: WorkItemQueryResult = self.__work_item_tracking_client.query_by_wiql(bugs, top=150).work_items
        print("work_items",work_items)
        if work_items:
        # WIQL query gives a WorkItemReference with ID only
        # => we get the corresponding WorkItem from id
            work_items = (
                self.__work_item_tracking_client.get_work_item(int(res.id)) for res in work_items
            )
            for work_item in work_items:
                print("work_item",work_item)
            return work_items
            
        raise Exception('Project ID not informed')

# work_item {'additional_properties': {}, 'url': 'https://pdasolucoes.visualstudio.com/03105f34-ffa4-48ca-b433-f6a2abd72cd7/_apis/wit/workItems/151', '_links': <azure.devops.v5_1.work_item_tracking.models.ReferenceLinks object at 0x000001B2471F44C0>, 'comment_version_ref': None, 'fields': {'System.AreaPath': 'Projetos', 'System.TeamProject': 'Projetos', 'System.IterationPath': 'Projetos', 'System.WorkItemType': 'Bug', 'System.State': 'Done', 'System.Reason': 'Work finished', 'System.AssignedTo': {'displayName': 'Rodrigo Mendonça', 'url': 'https://spsprodeus23.vssps.visualstudio.com/A0b316303-d5e1-4cd5-8ef9-013a1509f091/_apis/Identities/3aae20c5-65f8-46f2-980b-b9780445b030', '_links': {'avatar': {'href': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}}, 'id': '3aae20c5-65f8-46f2-980b-b9780445b030', 'uniqueName': 'rmendonca@pdasolucoes.com.br', 'imageUrl': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz', 'descriptor': 'aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}, 'System.CreatedDate': '2022-01-06T21:02:16.327Z', 'System.CreatedBy': {'displayName': 'Rodrigo Mendonça', 'url': 'https://spsprodeus23.vssps.visualstudio.com/A0b316303-d5e1-4cd5-8ef9-013a1509f091/_apis/Identities/3aae20c5-65f8-46f2-980b-b9780445b030', '_links': {'avatar': {'href': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}}, 'id': '3aae20c5-65f8-46f2-980b-b9780445b030', 'uniqueName': 'rmendonca@pdasolucoes.com.br', 'imageUrl': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz', 'descriptor': 'aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}, 'System.ChangedDate': '2022-02-04T18:38:40.127Z', 'System.ChangedBy': {'displayName': 'Rodrigo Mendonça', 'url': 'https://spsprodeus23.vssps.visualstudio.com/A0b316303-d5e1-4cd5-8ef9-013a1509f091/_apis/Identities/3aae20c5-65f8-46f2-980b-b9780445b030', '_links': {'avatar': {'href': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}}, 'id': '3aae20c5-65f8-46f2-980b-b9780445b030', 'uniqueName': 'rmendonca@pdasolucoes.com.br', 'imageUrl': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz', 'descriptor': 'aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}, 'System.CommentCount': 1, 'System.Title': 'expedicao raizs> "Ao coletar mais de uma caixa no mesmo endereço, cursor não retorna para a caixa"', 'System.BoardColumn': 'Done', 'System.BoardColumnDone': False, 'Microsoft.VSTS.Common.StateChangeDate': '2022-01-07T15:27:20.11Z', 'Microsoft.VSTS.Common.ClosedDate': '2022-01-07T15:27:20.11Z', 'Microsoft.VSTS.Common.ClosedBy': {'displayName': 'Rodrigo Mendonça', 'url': 'https://spsprodeus23.vssps.visualstudio.com/A0b316303-d5e1-4cd5-8ef9-013a1509f091/_apis/Identities/3aae20c5-65f8-46f2-980b-b9780445b030', '_links': {'avatar': {'href': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}}, 'id': '3aae20c5-65f8-46f2-980b-b9780445b030', 'uniqueName': 'rmendonca@pdasolucoes.com.br', 'imageUrl': 'https://pdasolucoes.visualstudio.com/_apis/GraphProfile/MemberAvatars/aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz', 'descriptor': 'aad.ZTBhZDkyZmUtMWI2ZS03YzliLTgxMjEtNjllNWU5MWRmMTEz'}, 'Microsoft.VSTS.Common.Priority': 3, 'Microsoft.VSTS.Common.Severity': '3 - Medium', 'Microsoft.VSTS.Common.ValueArea': 'Business', 'WEF_38DDEAE3F3AE495E88E8C5D4E8BF84DE_Kanban.Column': 'Done', 'WEF_38DDEAE3F3AE495E88E8C5D4E8BF84DE_Kanban.Column.Done': False, 'System.Tags': 'Coletores; expedicao'}, 'id': 151, 'relations': None, 'rev': 8}