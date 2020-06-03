# #imports
import json
from modules.project_managament.tool.hubspot import tool_api
from modules.project_managament.classes.extra_useful_classes import ToolEmployee, ToolTask
from modules.project_managament.classes import TaskHistory, Space, CompanyProjects, Employee, Project, Task, Tool
from configuration import classes_names, tools_keys, database_setting as db_set
from database import Database, methods
import psycopg2

# ---------------------------------------connect to database----------------------------------------
if __name__ == '__main__':
    # ---------------------------------------connect to database----------------------------------------
    db = Database.Database (db_set.database, db_set.user, db_set.password, db_set.host, db_set.port)
    try:
        connection = db.connection ()
        connection.autocommit = True
        cursor = connection.cursor ()
        print ("database ", db.name, "is opened")
    except:
        raise NameError ('failed to open the database')
    # --------------------------------------- insert Hubspot tool to tools table if it doesn't exist----------------------------------------
    try:
        tool = Tool.Tool (None, "HUBSPOT")  # set id into None because it is serial number in the database
        get_all_tools = methods.get_all (cursor, classes_names.tools)  # get all records in tool table
        if (len (get_all_tools) == 0):
            # insert record  into db and return ID
            tool.id = tool.insert_into_db (connection, cursor)
        else:
            is_found = False
            for i in range (len (get_all_tools)):
                if (get_all_tools[i][1] == tool.name):
                    is_found = True
                    tool.id = get_all_tools[i][0]
                    break
            if (is_found == False):
                tool.id = tool.insert_into_db (connection, cursor)

        get_all_projects = methods.get_all (cursor, classes_names.projects)  # DB_projects
        is_found = False
        for i in range (len (get_all_projects)):
            if (get_all_projects[i][2] == "HUBSPOT_Tasks"):
                is_found = True
                project_id = get_all_projects[i][0]
                break
        if (is_found == False):
            space = Space.Space (None, "HUBSPOT", tool.id, 0)
            space_id = space.insert_into_db (connection, cursor)
            project = Project.Project (None, space_id, "HUBSPOT_Tasks",
                                       None, None, None, None)
            project_id = project.insert_into_db (connection, cursor)
    except (Exception, psycopg2.DatabaseError) as error:
        print ("error in inserting Hubspot record in the tool table")
    # --------------------------------------- insert All the engagements in tasks table ----------------------------------------
    try:
        hubspot_tasks = tool_api.get_all_engagements ()  # get all the engagements from the API
        get_all_task_by_tool = ToolTask.get_by_tool_id (cursor, tool.id)  # get all the local engagements from the local database  that belongs to HUBSPORT
        tool_tasks_IDs = []
        local_hubspot_tasks = []
        for i in range (len (get_all_task_by_tool)):
            local_hubspot_tasks.append (get_all_task_by_tool[i][2])

        for x in range (len ((hubspot_tasks))):
            tool_tasks_IDs.append (str (hubspot_tasks[x]['engagement']['id']))
            if (str (hubspot_tasks[x]['engagement']['id']) not in local_hubspot_tasks):
                metadata = hubspot_tasks[x]['metadata']  # store the metadata of the task[x]
                if (hubspot_tasks[x]['engagement']['type'] == 'TASK'):  # if the engagement type is TASK
                    try:
                        TaskName = metadata['subject']
                    except:
                        TaskName=None
                else:
                    if (hubspot_tasks[x]['engagement']['type'] == 'NOTE'):  # if the engagement type is NOTE
                        TaskName = "NOTE : " + metadata['body']
                    else:
                        if (hubspot_tasks[x]['engagement']['type'] == 'EMAIL'):  # if the engagement type is EMAIL
                            try:
                                TaskName = "EMAIL TO  : " + metadata['to'][0]['email']
                            except:
                                try:
                                    TaskName = "EMAIL TO  : " + metadata['to'][0]['firstName']
                                except:
                                    TaskName = "empty"
                        else:
                            if (hubspot_tasks[x]['engagement']['type'] == 'MEETING'):  # if the engagement type is MEETING
                                TaskName = "meeting  : " + hubspot_tasks[x]['engagement']['bodyPreview']
                            else:
                                if (hubspot_tasks[x]['engagement']['type'] == 'CALL'):  # if the engagement type is CALL
                                    try:
                                        TaskName = "call to " + str (hubspot_tasks[x]['associations']['contactIds'][0])
                                    except:
                                        try:
                                            TaskName = "call to " + str (hubspot_tasks[x]['associations']['companyIds'][0])
                                        except:
                                            TaskName = "CALL "
                                else:
                                    if (hubspot_tasks[x]['engagement']['type'] == 'INCOMING_EMAIL'):  # if the engagement type is INCOMING_EMAIL
                                        TaskName = " INCOMING EMAIL TO  : " + metadata['from']['email']
                                    else:
                                        if (hubspot_tasks[x]['engagement']['type'] == 'FORWARDED_EMAIL'):  # if the engagement type is FORWARDED_EMAIL
                                            TaskName = " FORWARDED EMAIL TO  : " + metadata['to'][0]['email']

                var_employee_id = None
                # get the Employee ID stored in the database
                employee_id = ToolEmployee.get_employee_id \
                    (cursor, hubspot_tasks[x]['engagement']['ownerId'], tool.id)
                if (len (employee_id) != 0):  # if employee  exist in our database
                    var_employee_id = employee_id[0]
                else:
                    owner = tool_api.Get_owner (hubspot_tasks[x]['engagement']['ownerId'])

                    employee_id = Employee.get_id_by_name (cursor, owner['firstName'] + ' ' + owner['lastName'])
                    if (len (employee_id) != 0):  # if we found the employee by his /her name
                        var_employee_id = employee_id[0]
                    else:
                        tool_employee = ToolEmployee.ToolEmployee (var_employee_id, tool.id, owner["ownerId"])
                        tool_employee.insert_into_db(connection,cursor)
                createdAt=hubspot_tasks[x]['engagement']['createdAt']
                lastUpdated=hubspot_tasks[x]['engagement']['lastUpdated']
                active=hubspot_tasks[x]['engagement']['active']
                task = Task.Task (None, project_id,
                                  var_employee_id, TaskName, createdAt,
                                  lastUpdated, None, active,hubspot_tasks[x])
                task_id = task.insert_into_db (connection, cursor)
                Tool_task = ToolTask.ToolTask (task_id, tool.id, hubspot_tasks[x]['engagement']['id'])
                Tool_task.insert_into_db (connection, cursor)
            else:
                index = None
                for i in range (len (get_all_task_by_tool)):

                    if (get_all_task_by_tool[i][2] == str (hubspot_tasks[x]['engagement']['id'])):
                        index = i
                        break
                if (index != None):

                    createdAt = hubspot_tasks[x]['engagement']['createdAt']

                    lastUpdated = hubspot_tasks[x]['engagement']['lastUpdated']

                    active = hubspot_tasks[x]['engagement']['active']
                    Task.update_variables (connection, cursor, get_all_task_by_tool[index][0],
                                           lastUpdated, None,active)
        for x in range (len (local_hubspot_tasks)):
            if (local_hubspot_tasks[x] not in tool_tasks_IDs):
                index = None
                for i in range (len (local_hubspot_tasks)):
                    if (local_hubspot_tasks[x] == tool_tasks_IDs[i]):
                        index = i
                        break
                if (index != None):
                    Task.close_task (connection, cursor, local_hubspot_tasks[index])
    except:
        print ("error in Hubspot tool integration")
