import psycopg2
from configuration import classes_names

import json
def create_table():
    create_table_query = "CREATE TABLE  "+classes_names.recruitment+"" \
                     "(id  SERIAL PRIMARY KEY  NOT NULL," \
                     " job_position varchar,"\
                     " candidate_tool_id  varchar," \
                     " candidate_Name varchar," \
                     " interviewer_id integer REFERENCES "+classes_names.employee+"(id)," \
                     " interview_date integer REFERENCES  "+classes_names.calendar+"(id)," \
                     " stage  varchar , Note json , email varchar ,phone integer ); "
    return create_table_query
def InsertRecruitment(connnection, cursor,candidate_tool_id, jobPosition, name, Email,phone,stage,note):
    try:
        query = "INSERT INTO "+classes_names.recruitment+"(candidate_tool_id,job_position, candidate_Name, email,phone,stage,Note)VALUES(%s,%s,%s,%s,%s,UPPER(%s),%s);"
        cursor.execute (query, (candidate_tool_id,jobPosition, name, Email,phone,stage,note,))
        connnection.commit ()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during inserting into Recruitment table , ERROR : ", error)


def update(connnection, cursor,id, stage):
    try:
        query = " SELECT candidate_tool_id,upper(stage) from " + classes_names.recruitment + " where upper (candidate_tool_id) =  upper(%s) ;"
        cursor.execute (query, id,)
        query_result = cursor.fetchall ()
        # print(query_result[0][0],query_result[0][1])

        if (len (query_result) != 0):

            if(query_result[0][1]!=stage):
                create_query = " UPDATE " + classes_names.recruitment + " set stage = upper(%s) where upper (candidate_tool_id) =  upper(%s)  ;"
                cursor.execute (create_query, (str(stage),id,) )
                connnection.commit ()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during updating into Recruitment table , ERROR : ", error)
def getLocalCandidates(connnection, cursor):
    try:
        candidates=[]
        query = " SELECT candidate_tool_id from " + classes_names.recruitment+" ;"
        cursor.execute (query )
        query_result = cursor.fetchall ()
        for x in range(len(query_result)):
            candidates.append(query_result[x][0])
        return candidates


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getLocalCandidates function , ERROR : ", error)


def getById(connnection, cursor,id):
    try:

        query = " SELECT * from " + classes_names.recruitment + " where id=%s ;"
        cursor.execute (query,id,)
        query_result = cursor.fetchall ()
        recruitment = []
        if (len (query_result)!=0) :


                recruitment=\
                    {"ID": query_result[0][0],
                     "candidate-tool_id ": query_result[0][1],
                     "job_position":query_result[0][2],
                     "candidate_name":query_result[0][3],
                     "interviewer_id":query_result[0][4],
                     "interview_date":query_result[0][5],
                     "stage":query_result[0][6],
                     "Note":query_result[0][7],
                     "email":query_result[0][8],
                     "phone":query_result[0][9]}
                return json.dumps(recruitment)
        else: return  []


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)

def getAll(connnection, cursor):
    try:

        query = " SELECT * from " + classes_names.recruitment + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        recruitments = []
        if (len (query_result)!=0) :

            for x in range(len (query_result)):
                recruitment=\
                    {"ID": query_result[x][0],
                     "candidate-tool_id ": query_result[x][1],
                     "job_position":query_result[x][2],
                     "candidate_name":query_result[x][3],
                     "interviewer_id":query_result[x][4],
                     "interview_date":query_result[x][5],
                     "stage":query_result[x][6],
                     "Note":query_result[x][7],
                     "email":query_result[x][8],
                     "phone":query_result[x][9]}
                recruitments.append(recruitment)

        Result_json = {"recruitments": recruitments}
        return json.dumps(Result_json)


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)
