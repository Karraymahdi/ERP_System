from configuration import classes_names
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.spaces + "" \
  "(id SERIAL PRIMARY KEY     NOT NULL," \
  "name VARCHAR NOT NULL," \
  "tool_id integer  REFERENCES " + classes_names.tools + "(id)," \
  "tool_space_id integer NOT NULL );"
    return create_table_query
class Space:
    def __init__(self,id,name,tool_id,tool_space_id):
        self.id=id
        self.name=name
        self.tool_id=tool_id
        self.tool_space_id=tool_space_id

    def insert_into_db(self, connection, cursor):
        try:
            query = "INSERT INTO " + classes_names.spaces + "(name,tool_id,tool_space_id)VALUES(%s,%s,%s) RETURNING id;"
            cursor.execute (query,(self.name,self.tool_id,self.tool_space_id,))
            connection.commit()
            query_result = cursor.fetchone ()
            return query_result[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Exception during inserting into space table , ERROR : ", error)
            raise NameError ('failed to insert the space record ', error)


    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_tool_id(self):
        return self.tool_id
    def get(self):
        return self.tool_space_id
