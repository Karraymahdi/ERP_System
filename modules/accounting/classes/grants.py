import psycopg2
from configuration import classes_names
import json
create_table_query = "CREATE TABLE "+classes_names.grants+"" \
                     "(local_id SERIAL PRIMARY KEY     NOT NULL," \
                     "title varchar ," \
                     "total_amount double precision," \
                     "currency varchar ); "

def getById(connnection, cursor, id):
    try:

        query = " SELECT * from " + classes_names.grants + " where local_id=%s ;"
        cursor.execute (query, id, )
        query_result = cursor.fetchall ()
        if (len (query_result) != 0):

            grant = \
                {"ID": query_result[0][0],
                 "title ": query_result[0][1],
                 "total_amount": query_result[0][2],
                 "currency": (query_result[0][3])}
            return json.dumps (grant)
        else:
            return []


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during get By ID function , ERROR : ", error)


def getAll(connnection, cursor):
    try:

        query = " SELECT * from " + classes_names.grants + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        grants = []
        if (len (query_result) != 0):

            for x in range (len (query_result)):
                if (len (query_result) != 0):
                    grant = \
                        {"ID": query_result[0][0],
                         "title ": query_result[0][1],
                         "total_amount": query_result[0][2],
                         "currency": (query_result[0][3])}
                grants.append (grant)

        Result_json = {"grants": grants}
        return json.dumps (Result_json)


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)
