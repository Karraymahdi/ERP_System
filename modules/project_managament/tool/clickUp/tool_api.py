#imports
import psycopg2
import requests
from datetime import datetime
from configuration import tools_keys
#---------------------------------------click up access----------------------------------------

#headers
headers = {
  'Authorization': tools_keys.clickup_Key
}
#api
API="https://api.clickup.com/api/v1/"#api_url
#---------------------------------------click up API----------------------------------------
# Get Team'id
def GetTeamId():
    response = requests.get (API + 'team', headers=headers)
    team = response.json ()
    team_id = team['teams'][0]['id']
    return team_id

#Team's spaces
def GetTeamSpaces(teamID):
    response = requests.get(API +'team/' +teamID+ '/space', headers=headers)
    Spaces = (response.json())['spaces']
    return Spaces

#Get Projects (List are attached to projects metadata)
def GetProjects(spaceID):
        response = requests.get(API + 'space/'+str(spaceID)+'/project', headers=headers)
        projects = (response.json())['projects']
        return projects
#Get tasks
def GetTasks(teamID):
         response = requests.get (API + 'team/' + str(teamID) + '/task', headers=headers)
         tasks = (response.json())['tasks']
         return tasks


#---------------------------------------Testing----------------------------------------

