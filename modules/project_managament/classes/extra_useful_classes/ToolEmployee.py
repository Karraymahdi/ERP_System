from configuration import classes_names

import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.tool_employee_id + " " \
    "(employee_id integer REFERENCES " + classes_names.employee + "(id)  NULL," \
    "tool_id int REFERENCES " + classes_names.tools + "(id)," \
    "tool_employee_id integer ); "
    return create_table_query
def get_employee_id(cursor,tool_employee_id,tool_id):
    try:
        query = " SELECT employee_id from "+classes_names.tool_employee_id+\
                " where (tool_employee_id)= (%s) " \
                " and  (tool_id)= (%s);"
        cursor.execute (query, (tool_employee_id, tool_id,))
        query_result = cursor.fetchone()
        if(query_result==None):
            return []
        return query_result
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Exception appears while calling get_employee_id ",error)
def get_by_tool_id(cur,tool_id):
    try:
        var = []
        query = "SELECT * from "+classes_names.tools_tasks_id+" where tool_id = %s;"
        cur.execute (query,(tool_id,))
        query_result = cur.fetchall ()
        if (len (query_result) != 0):
            for x in range (len (query_result)):
                var.append (query_result[x])
        return var
    except (Exception, psycopg2.DatabaseError)\
            as error:
        print("Exception appears while calling get_by_tool_id method , ERROR :  " ,error)

class ToolEmployee:
    def __init__(self,employee_id,tool_id,tool_employee_id):
        self.employee_id=employee_id
        self.tool_id=tool_id
        self.tool_employee_id=tool_employee_id

    def insert_into_db(self, connection, cursor):
        try:
            query = "INSERT INTO " + classes_names.tool_employee_id + " (employee_id,tool_id," \
                                                               " tool_employee_id) VALUES(%s,%s,%s) ;"
            cursor.execute (query, (self.employee_id, self.tool_id, self.tool_employee_id,))
            connection.commit ()
        except (Exception, psycopg2.DatabaseError) as error:
            raise NameError ('failed to insert the Task  record ', error)

