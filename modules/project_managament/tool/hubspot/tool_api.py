import requests
from configuration import tools_keys
API='https://api.hubapi.com/engagements/v1/engagements/paged'
hapikey= tools_keys.Hubspot_key
def get_all_engagements():
    response = requests.get (API,
                             params={'hapikey': hapikey , 'limit': '250'})
    result = (response.json ()['results'])
    hubspot_tasks = []
    for x in range (len (result)):
         hubspot_tasks.append (result[x])

    has_more=False
    offset=None
    if (response.json ()['hasMore'] == True):
        has_more = True
        offset = response.json ()['offset']
    while(has_more==True):
        #if (response.json ()['hasMore'] == True):
        response1 = requests.get (API,
                                  params={'hapikey':hapikey,
                                          'offset': offset})
        result = (response1.json ()['results'])
        for x in range (len (result)):
               hubspot_tasks.append (result[x])
        if (response1.json ()['hasMore'] == True):
            offset = response1.json ()['offset']
        else:
            has_more=False
            offset=None
    return hubspot_tasks

def Get_owner(ownerid):
    response = requests.get ('http://api.hubapi.com/owners/v2/owners/'+str(ownerid),
                             params={'hapikey': hapikey})
    result = (response.json ())
    return result
def get_all_contact():
    contacts=[]
    response = requests.get ('https://api.hubapi.com/contacts/v1/lists/all/contacts/all',
                             params={'hapikey': hapikey,'count': 100})
    result = (response.json()['contacts'])
    for x in range (len (result)):
        contacts.append (result[x])

    if (response.json ()['has-more'] == True):
        has_more = True
        offset = response.json ()['vid-offset']
    else:
        has_more = False

    while (has_more != False):

        response1 = requests.get ('https://api.hubapi.com/contacts/v1/lists/all/contacts/all',
                                  params={'hapikey': hapikey,'count': 100,
                                          'vidOffset': offset})
        result = (response1.json ()['contacts'])
        for x in range (len (result)):
            contacts.append (result[x])
        if (response1.json ()['has-more'] == True):
            offset = response1.json ()['vid-offset']
        else:
            has_more = False
            offset = None
    return contacts
#
# a=get_all_engagements()
# print(len(a))
# # print(Get_owner())
# contacts=get_all_contact()
# print(len(contacts))

