#imports
import json
import psycopg2
from modules.toolsAPI import brezzyAPI
from Tables.tools import  tools
from Tables.hr import recruitment
from DatabaseConnection import database_connection
from config import config

#---------------------------------------connect to database----------------------------------------

try:#try to connect to the database

    try:
        con = database_connection.connection ()
        cur = con.cursor ()
    except:
        print("fail to open the database")



#--------------------------------------- insert BREZZY tool to tools table if it doesn't exist----------------------------------------

    try:
        query_result= tools.GetToolID(con, cur, "BREZZY")
        if(len(query_result)==0):
            tools.InsertTool (con, cur, "BREZZY")
            query_result = tools.GetToolID (con, cur, "BREZZY")
            toolId = query_result[0][0]
        else:
            toolId=query_result[0][0]

    except (Exception, psycopg2.DatabaseError) as error:
       print(error)
    print (toolId)


#--------------------------------------- Get BREZZY tool access ----------------------------------------
    try:
       brezzyAPI.access()
    except(Exception)as error:
       print("error when getting access from BREZZY tool  : ",error)


#--------------------------------------- Get company id from BREZZY tool  ----------------------------------------
    try:
        companies=[]
        companies=brezzyAPI.GetCompany()
        CompanyExist=False
        if(len(companies)>0):
            CompanyExist=True
            company=companies[0]
        else:
            print("There is no Company exist ")

    except(Exception)as error:
       print("error during  getting company id  from BREZZY tool  : ",error)

# --------------------------------------- CHECK IF THERE IS COMPANY DATA  ----------------------------------------
#here if we don't have any company data exist then we can't get any positions or candidate

    if (CompanyExist == True):
        positions=[]
#--------------------------------------- Get positions from BREZZY tool  ----------------------------------------

        try:

                #positions when the state of it is "draft"
                positions_response=brezzyAPI.GetPositions(company['_id'],'draft')
                if(len(positions_response)>0):
                    for x in range (len(positions_response)):
                        positions.append(positions_response[x])
                #positions when the state of it is "archived"
                positions_response = brezzyAPI.GetPositions (company['_id'], 'archived')
                if (len (positions_response) > 0):
                    for x in range (len(positions_response)):
                        positions.append(positions_response[x])
                #positions when the state of it is "published"
                positions_response = brezzyAPI.GetPositions (company['_id'], 'published')
                if (len (positions_response) > 0):
                    for x in range (len(positions_response)):
                        positions.append(positions_response[x])
                #positions when the state of it is "closed"
                positions_response = brezzyAPI.GetPositions (company['_id'], 'closed')
                if (len (positions_response) > 0):
                    for x in range (len(positions_response)):
                        positions.append(positions_response[x])
                #positions when the state of it is "pending"
                positions_response = brezzyAPI.GetPositions (company['_id'], 'pending')
                if (len (positions_response) > 0):
                    for x in range (len(positions_response)):
                        positions.append(positions_response[x])

                print(positions)
        except(Exception)as error:
           print("error during  getting positions from BREZZY tool  : ",error)


#--------------------------------------- Get candidates from BREZZY tool  ----------------------------------------


        try:
            if len(positions)>0:
                candidates=recruitment.getLocalCandidates()
                for x in range (len(positions)):
                 candidates_response=brezzyAPI.GetCandidates(company['_id'],positions[x]['_id'])
                 if(len(candidates_response)>0):
                    for y in range(len(candidates_response)):
                        if (candidates_response[y]['_id'] not in candidates):
                          recruitment.InsertRecruitment(con,cur,candidates_response[y]['_id'],positions[x]['name'],
                                                      candidates_response[y]['name'],candidates_response[y]['email_address'],
                                                      candidates_response[y]['phone_number'],
                                                      candidates_response[y]['stage']['name'],None )
                        else:
                            #Update method is going to update the stage of the recruitment if it is changed
                           recruitment.update(con,cur,candidates_response[y]['_id'],
                                              candidates_response[y]['stage']['name'])



        except(Exception)as error:
            print ("error during  getting candidates from BREZZY tool  : ", error)






except:
    None