from configuration import classes_names

import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " \
 + classes_names.company_projects + \
 "(id SERIAL PRIMARY KEY NOT NULL," \
 " project_id integer REFERENCES " \
 + classes_names.projects + "(id)," \
 " company_name VARCHAR ," \
 " company_id varchar); "
    return create_table_query
def get_project_id(cursor,company_id):
    try:
        query = " SELECT project_id from "+classes_names.company_projects+" where company_id = (%s) ;"
        cursor.execute (query, (str(company_id),))
        query_result = cursor.fetchall ()
        if (len (query_result) != 0):
            return query_result[0][0]
        else:
            return None
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Exception appers while calling GetlocalProjectID from companyProject ",error)

class CompanyProjects:
    def __init__(self, id, project_id, company_name, company_id):
        self.id = id
        self.project_id = project_id
        self.company_name = company_name
        self.company_id = company_id


    # def GetlocalProjectID(connection, cursor, companyID):
    #     try:
    #         query = " SELECT id from " + config.company_projects + " where companyID =  (%s) ;"
    #         cursor.execute (query, (str (companyID),))
    #         query_result = cursor.fetchall ()
    #         if (len (query_result) != 0):
    #             return query_result[0][0]
    #         else:
    #             return None
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print ("Exception appers while calling GetlocalProjectID from companyProject ", error)

    def get_id(self):
        return self.id
    def set_id(self,id):
        self.id=id
    def get_project_id(self):
        return self.project_id
    def set_project_id(self,project_id):
        self.project_id=project_id
    def get_company_name(self):
        return self.company_name
    def set_company_name(self,company_name):
        self.company_name=company_name
    def get_company_id(self):
        return self.company_id
    def set_company_name(self,company_id):
        self.company_id=company_id