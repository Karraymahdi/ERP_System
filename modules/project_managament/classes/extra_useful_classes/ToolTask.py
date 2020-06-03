from configuration import classes_names
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.tools_tasks_id + "" \
    "(task_id integer REFERENCES " + classes_names.tasks + "(id)," \
    "tool_id integer REFERENCES " + classes_names.tools + "(id)," \
    "tool_task_id VARCHAR   NOT NULL    ); "
    return create_table_query
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
class ToolTask:
    def __init__(self,task_id,tool_id,tool_task_id):
        self.task_id=task_id
        self.tool_id=tool_id
        self.tool_task_id=tool_task_id

    def insert_into_db(self, connection, cursor):
            try:
                create_query = "INSERT INTO  " + classes_names.tools_tasks_id + "(task_id,tool_id,tool_task_id)VALUES(%s,%s,%s);"
                cursor.execute (create_query, (self.task_id,self.tool_id,self.tool_task_id,))
                connection.commit ()

            except (Exception, psycopg2.DatabaseError) as error:
                raise NameError ('failed to insert the Task  record ', error)





