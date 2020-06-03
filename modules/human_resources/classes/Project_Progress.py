from configuration import classes_names
import json
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE  "+classes_names.project_progress+"" \
                     "(id  SERIAL PRIMARY KEY  NOT NULL," \
                     " project_id integer REFERENCES "+classes_names.projects+"(id)," \
                     " employee_id integer REFERENCES "+classes_names.employee+"(id)," \
                     " day_id integer REFERENCES  "+classes_names.calendar+"(id)," \
                     " percentage integer); "
    return create_table_query



def getAll(connnection, cursor):
    try:
        query = " SELECT * from " + classes_names.project_progress + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        projects_progress = []
        if (len (query_result)!=0) :

            for x in range(len (query_result)):
                project_progress=\
                    {"ID": query_result[x][0],
                     "projectID ": query_result[x][1],
                     "employeeID":query_result[x][2],
                     "dayid":query_result[x][3],
                     "percentage":query_result[x][4]
                     }
                projects_progress.append(project_progress)

        Result_json = {"projects_progress": projects_progress}
        return json.dumps(Result_json)
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)

def getById(connnection, cursor,id):
    try:
        query = " SELECT * from " + classes_names.project_progress + " where id=%s ;"
        cursor.execute (query,id,)
        query_result = cursor.fetchall ()

        if (len (query_result) != 0):

            for x in range (len (query_result)):
                project_progress = \
                    {"ID": query_result[0][0],
                     "projectID ": query_result[0][1],
                     "employeeID": query_result[0][2],
                     "dayid": query_result[0][3],
                     "percentage": query_result[0][4]
                     }
            return json.dumps (project_progress)
        else: return  []

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getById function , ERROR : ", error)


