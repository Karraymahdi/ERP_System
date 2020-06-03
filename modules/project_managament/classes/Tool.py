from configuration import classes_names
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.tools + \
                         "(id SERIAL PRIMARY KEY NOT NULL," \
                         " name VARCHAR    NOT NULL ); "
    return create_table_query

class Tool :
    def __init__(self,id,name):
        self.id=id
        self.name=name

    def insert_into_db(self,connnection, cursor):
        try:
            query = "INSERT INTO " + classes_names.tools + "(name)VALUES(%s) RETURNING id ;"
            cursor.execute (query, (self.name,))
            connnection.commit ()
            query_result = cursor.fetchone ()
            return query_result[0]
        except (Exception, psycopg2.DatabaseError) as error:
            raise NameError ('failed to insert the tool record ',error)
            print ("Exception during inserting into Tool table , ERROR : ", error)
