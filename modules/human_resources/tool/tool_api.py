#imports
import psycopg2
import requests
from datetime import datetime
from configuration import tools_config
#---------------------------------------Brezzy access----------------------------------------

#headers
headers = {
  'Authorization': tools_config.Brezzy_Key,
  'Content-Type':'application/x-www-form-urlencoded'
}
#api
API="https://api.breezy.hr/v3/"#api_url
#user
UserID=""
#---------------------------------------Brezzy API----------------------------------------
# Get access
def access ():

    # data to be sent to api
    data = {'email':'************','password':''}
    response = requests.post (API + 'signin', data=data)
    access = response.json ()
    print(access['user']['_id'])
    tools_config.Brezzy_Key = access['access_token']
    UserID=access['user']['_id']

# Get company
def GetCompany():
    response = requests.get (API + 'companies', headers=headers)
    response = response.json ()
    return response

# Get positions
def GetPositions(companyID,state):
    response = requests.get (API + 'company/'+companyID+'/positions', params={'state': state},headers=headers)
    response = response.json ()
    return response



# Get candidates
def GetCandidates(companyID,positionID):
    response = requests.get (API + 'company/'+companyID+'/position/'+positionID+'/candidates',headers=headers)
    response = response.json ()
    return response

