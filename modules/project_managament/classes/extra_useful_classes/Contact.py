from configuration import classes_names
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.contact+ " " \
    "(id SERIAL PRIMARY KEY     NOT NULL," \
    "tool_contact_id integer," \
    "name varchar," \
    "email varchar," \
    "company varchar," \
    "preferred_Lanugage varchar," \
    "membership_notes varchar," \
    "tool_id int REFERENCES " + classes_names.tools + "(id) );"
    return create_table_query
class contact:
    def __init__(self,id,tool_contact_id,name,email,company,preferred_Lanugage,Membership_notes,tool_id):
        self. id=id
        self. tool_contact_id=tool_contact_id
        self. name=name
        self. email=email
        self. company=company
        self. preferred_Lanugage=preferred_Lanugage
        self. Membership_notes=Membership_notes
        self. tool_id=tool_id

    def insert_into_db(self, connection, cursor):
        try:
            query = "INSERT INTO " + classes_names.contact + "(tool_contact_id,name,email,company,preferred_Lanugage,Membership_notes,tool_id)" \
                                                             "VALUES(%s,%s,%s,%s,%s,%s,%s)" \

            cursor.execute (query, (self.tool_contact_id,self.name,self.email,self.company,self.preferred_Lanugage,self.Membership_notes,self.tool_id,))
            connection.commit ()
        except (Exception, psycopg2.DatabaseError) as error:
            raise NameError ('failed to insert the Task record ', error)



