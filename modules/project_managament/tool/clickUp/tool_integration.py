# imports
import json
from modules.project_managament.tool.clickUp import tool_api
from modules.project_managament.classes.extra_useful_classes import ToolEmployee, ToolTask
from modules.project_managament.classes import TaskHistory, Space, CompanyProjects, Employee, Project, Task, Tool
from configuration import classes_names, tools_keys, database_setting as db_set
from database import Database, methods
import psycopg2

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
        print ("failed to open the database")
    # --------------------------------------- insert clickUp tool to tools table if it doesn't exist----------------------------------------
    try:
        tool = Tool.Tool (None, "CLICKUP")  # set id into None because it is serial number in the database
        get_all_tools = methods.get_all (cursor, classes_names.tools)  # get all records in tool table
        if (len (get_all_tools) == 0):
            tool.id = tool.insert_into_db (connection, cursor)  # insert recorod into db and return ID
        else:
            is_found = False
            for i in range (len (get_all_tools)):
                if (get_all_tools[i][1] == tool.name):
                    is_found = True
                    tool.id = get_all_tools[i][0]
                    break
            if (is_found == False):
                tool.id = tool.insert_into_db (connection, cursor)
    except (Exception, psycopg2.DatabaseError) as error:
        raise NameError ('failed during inserting or getting clickUp tool ')
    # --------------------------------------- insert spaces into database ----------------------------------------
    try:
        tool_spaces = tool_api.GetTeamSpaces (tool_api.GetTeamId ())  # get all the spaces from the tool
        get_all_spaces = methods.get_all (cursor, classes_names.spaces)  # get all the record of the spaces table from the database
        for x in range (len (tool_spaces)):
            is_found = False

            for i in range (len (get_all_spaces)):
                tool_space_id = get_all_spaces[i][3]
                if (tool_space_id == int (tool_spaces[x]['id'])):
                    is_found = True
                    print ("Space exist")
                    break
            if (is_found == False):
                space = Space.Space (None, tool_spaces[x]['name'], tool.id, tool_spaces[x]['id'])
                space.insert_into_db (connection, cursor)

    except(Exception, psycopg2.DatabaseError) as error:
        print (error)
    # --------------------------------------- insert projects into database ----------------------------------------
    try:
        get_all_spaces = methods.get_all (cursor, classes_names.spaces)  # get all the record of the spaces table from the database
        Spaces = []  # store all the spaces belogns to clickUp tool
        for x in range (len (get_all_spaces)):
            var = get_all_spaces[x]
            if (var[2] == tool.id):
                space = Space.Space (var[0], var[1], var[2], var[3])
                Spaces.append (space)
        all_projects_tool = []  # all the projects in the tool
        get_all_projects = methods.get_all (cursor, classes_names.projects)  # DB_projects
        for x in range (len (Spaces)):
            spaceProjects = (tool_api.GetProjects (Spaces[x].tool_space_id))
            for y in range (len (spaceProjects)):
                all_projects_tool.append (spaceProjects[y])
                is_found = False
                for i in range (len (get_all_projects)):
                    tool_project_id = get_all_projects[i][3]
                    if ((tool_project_id) == int (spaceProjects[y]['id'])):
                        is_found = True
                        print ("project exist")
                        break
                if (is_found == False):
                    project = Project.Project (None, Spaces[x].id, spaceProjects[y]['name'],
                                               spaceProjects[y]['id'], None, None,
                                               json.dumps (spaceProjects[y]))
                    project.insert_into_db (connection, cursor)
        # Updating the archived projects
        get_all_projects = methods.get_all (cursor, classes_names.projects)  # DB_projects
        for x in range (len (get_all_projects)):
            is_found = False
            tool_project_id = get_all_projects[x][3]
            for i in range (len (all_projects_tool)):
                if (tool_project_id == int (all_projects_tool[i]['id'])):
                    is_found = True
                    break
            if (is_found == False):
                try:
                    create_query = " UPDATE   " + classes_names.projects + \
                                   " set archived = TRUE WHERE tool_project_id=%s;"  # get all Clickup IDs in local database
                    cursor.execute (create_query, (tool_project_id,))
                    connection.commit ()
                except (Exception, psycopg2.DatabaseError) as error:
                    print ("Error while updating archived variable in project table", error)

    except(Exception, psycopg2.DatabaseError) as error:
        print ("Exception in project section | error : ", error)

    #--------------------------------------- insert tasks into database ----------------------------------------
    try:
         get_all_task_by_tool=ToolTask.get_by_tool_id(cursor,tool.id)
         tool_tasks = tool_api.GetTasks (tool_api.GetTeamId())
         tool_tasks_IDs=[] #store all the ID's of the task which exsit in the tool
         for x in range (len (tool_tasks)):
             tool_tasks_IDs.append((tool_tasks[x]['id']))
             is_found=False
             for i in range(len(get_all_task_by_tool)):
                if (tool_tasks[x]['id']==get_all_task_by_tool[i][2]):
                    is_found=True
                    index=i
                    break
             if (is_found == False):
                 var_employee_id = None

                 employee_id = ToolEmployee.get_employee_id \
                     (cursor,tool_tasks[x]['creator']['id'], tool.id)
                 if (len(employee_id)!= 0):
                     var_employee_id=employee_id[0]
                 else:
                     employee_id = Employee.get_id_by_name (cursor, tool_tasks[x]['creator']['username'])
                     if (len (employee_id) != 0):
                         var_employee_id = employee_id[0]
                     else:
                         tool_employee=ToolEmployee.ToolEmployee(var_employee_id,tool.id, tool_tasks[x]['creator']['id'])
                         tool_employee.insert_into_db(connection,cursor)
                 for i in range(len(get_all_projects)):
                     if(get_all_projects[i][3]==int(tool_tasks[x]['project']['id'])):
                         project_id=get_all_projects[i][0]
                 task = Task.Task (None, project_id,
                                   var_employee_id, tool_tasks[x]['name'], tool_tasks[x]['date_created'],
                                   tool_tasks[x]['date_updated'], tool_tasks[x]['date_closed'],
                                   tool_tasks[x]['status']['status'], tool_tasks[x])
                 task_id = task.insert_into_db (connection, cursor)
                 Tool_task = ToolTask.ToolTask (task_id, tool.id, tool_tasks[x]['id'])
                 Tool_task.insert_into_db(connection, cursor)
             else:
                Task.update_variables(connection,cursor,get_all_task_by_tool[index][0],tool_tasks[x]['date_updated']
                                            ,tool_tasks[x]['date_closed'],
                                              tool_tasks[x]['status']['status'])
         get_all_tasks=ToolTask.get_by_tool_id(cursor,tool.id)
         for x in range (len (get_all_tasks)):
             if (get_all_tasks[x][2] not in tool_tasks_IDs):
                 Task.close_task (connection, cursor, get_all_tasks[x][0])

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Error while inserting tasks table", error)
