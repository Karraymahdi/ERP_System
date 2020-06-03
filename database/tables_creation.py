from database import Database,methods
from configuration import classes_names,tools_keys,database_setting as db_set
from modules.project_managament.classes import TaskHistory,Space,CompanyProjects,Employee,Project,Task,Tool
from modules.project_managament.classes.extra_useful_classes import ToolEmployee,ToolTask
from modules.human_resources.classes import calendar,Project_Progress,recruitment,paidLeave,Holidays
from modules.accounting.classes import incoming_invoices,outgoing_invoices,payroll,cash_flow,grants
import psycopg2

def tables_creation(connection, cursor):
        # # creation of tools table
        # try:
        #     methods.execute_query(connection,cursor,Tool.create_table())
        #
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating tool table", error)
        # # creation of spaces table
        # try:
        #     methods.execute_query (connection, cursor, Space.create_table())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating Spaces table", error)
        #
        # # creation of projects table
        # try:
        #     methods.execute_query (connection, cursor, Project.create_table())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating project table", error)
        # # creation of employee table
        # try:
        #     methods.execute_query (connection, cursor, Employee.create_table ())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating employee table", error)
        #
        # # creation of ToolEmployee table
        # try:
        #     methods.execute_query (connection, cursor, ToolEmployee.create_table())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating ToolEmployee table", error)
        #
        # # creation of task table
        # try:
        #     methods.execute_query (connection,cursor,Task.create_table ())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating task table", error)
        #
        #     # creation of company_Projects table
        # try:
        #     methods.execute_query (connection, cursor, CompanyProjects.create_table ())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating CompanyProjects table", error)
        #
        # # creation of ToolTask table
        # try:
        #     methods.execute_query (connection, cursor, ToolTask.create_table ())
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating ToolTask table", error)
        #
        #     # creation of task_history table
        # try:
        #     methods.execute_query (connection, cursor, TaskHistory.create_table ())
        #     methods.execute_query (connection, cursor, TaskHistory.procedure_update)
        #     methods.execute_query (connection, cursor, TaskHistory.create_trigger_update)
        #     methods.execute_query (connection, cursor, TaskHistory.procedure_insert)
        #     methods.execute_query (connection, cursor, TaskHistory.create_trigger_insert)
        #
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print ("Error while creating task_history table", error)

        # creation of calendar table

        try:
            methods.execute_query (connection, cursor, calendar.create_table())
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating calendar table", error)

        # creation of paid leave table
        try:
            methods.execute_query(connection, cursor,paidLeave.create_table())
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating paid leave table", error)
        # creation of Project progress table
        try:
            methods.execute_query(connection, cursor,Project_Progress.create_table())
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating Project progress table", error)
        # creation of recruitment  table
        try:
            methods.execute_query(connection, cursor,recruitment.create_table())
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating recruitment progress table", error)
        # -----------------Accounting
        # creation of incoming invoices table
        try:
            methods.execute_query(connection, cursor,incoming_invoices.create_table_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating incoming_invocies  table", error)
        # creation of outgoing invoives table
        try:
            methods.execute_query (connection, cursor,outgoing_invoices.create_table_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating outgoing_invoices  table", error)
        # creation of cash_flow  table
        try:
            methods.execute_query (connection, cursor,cash_flow.create_table())
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating cash_flow  table", error)
        # creation of grants  table
        try:
            methods.execute_query (connection, cursor,grants.create_table_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating grants  table", error)

        # creation of payroll  table
        try:
            methods.execute_query (connection, cursor,payroll.create_table_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating payroll  table", error)

        cursor.close ()
        connection.close ()

if __name__ == '__main__':

    db=Database.Database(db_set.database, db_set.user, db_set.password, db_set.host, db_set.port)
    try:
        connection=db.connection()
        connection.autocommit = True
        cursor = connection.cursor ()
        print("done")
        query = "ALTER DATABASE  " + db_set.database + " SET timezone TO 'Europe/Budapest';"
        methods.execute_query(connection,cursor,query)
        tables_creation(connection,cursor)

    except:
        print ("fail to open the database")








    # dropAllTables(con,cursor)
    # tablesCreation (con, cursor)