import psycopg2
from configuration import classes_names,tools_keys,database_setting as db_set
from database import Database, methods
def drop_all_tables(connection, cursor):
    query = """DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public
    ;"""
    try:
        cursor.execute (query)
        connection.commit ()
    except(Exception, psycopg2.DatabaseError) as error:
        print ("Error while dropping the tables", error)

def execute_query(connection, cursor, query):
    try:
        cursor.execute (query)
        connection.commit ()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Error while executing the query | error : ", error)
        return False


def get_by_id(cursor,table_name,id):
        try:
            query = " SELECT * from " + table_name + " where id =%s ;"
            cursor.execute (query, id, )
            query_result = cursor.fetchall ()
            return query_result
            if (len (query_result) != 0):
                return query_result
            else: return []
        except (Exception, psycopg2.DatabaseError) as error:
         raise NameError ('Exception during get_by_id function ',error)
         print ("Exception during get_by_id function , ERROR : ", error)


def get_all(cursor,table_name):
    try:
        query = " SELECT * from " + table_name + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()

        if (len (query_result) != 0):
            return query_result
        else:
            return []
    except (Exception, psycopg2.DatabaseError) as error:
        raise NameError ('Exception during get_all function ', error)
        print ("Exception during get_all function , ERROR : ", error)
if __name__ == '__main__':

    db=Database.Database(db_set.database, db_set.user, db_set.password, db_set.host, db_set.port)
    # db.create()
    # open the created database
    try:
        connection=db.connection()
        connection.autocommit = True
        cursor = connection.cursor ()
        drop_all_tables(connection,cursor)

    except:
        print ("fail to open the database")

