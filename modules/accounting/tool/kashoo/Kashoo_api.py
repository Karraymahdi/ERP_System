from configuration import tools_keys
import requests

#---------------------------------------kashoo access----------------------------------------

#headers
headers = {
  'Authorization': "TOKEN uuid:"+tools_keys.kashoo_token,
   'Content-Type': "application/json",
    'Accept':"application/json"
}
#api
API="https://api.kashoo.com/api/"#api_url

def get_all_bills():
    response = requests.get (API + 'businesses/'+tools_keys.kashoo_company_id+"/records/bills"
                             , headers=headers)
    bills = response.json ()
    return bills

