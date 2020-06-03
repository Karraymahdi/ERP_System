from configuration import classes_names
import json
from datetime import datetime
from pytz import timezone
import psycopg2


def create_table():
    create_table_query = "CREATE TABLE " + classes_names.tasks + "" \
                                                                 "(id SERIAL PRIMARY KEY     NOT NULL," \
                                                                 " project_id integer REFERENCES  "\
                         + classes_names.projects + "(id)," \
                                                    " employee_id integer REFERENCES  " \
                         + classes_names.employee + "(id)," \
                                                    " name VARCHAR  NULL,created TIMESTAMP ," \
                                                    " updated TIMESTAMP,closed TIMESTAMP ," \
                                                    " status varchar ,metadata json);"
    return create_table_query

def update_variables(con, cur, id, updated, closed, status):
    query = " SELECT updated from " + classes_names.tasks + " where id =%s ;"
    cur.execute (query, (id,))
    query_result = cur.fetchall ()
    time1 = datetime.strptime (str (query_result[0][0]), '%Y-%m-%d %H:%M:%S')
    time2 = (datetime.fromtimestamp ((int (updated) / 1000), tz=timezone ('Europe/Budapest')).replace (tzinfo=None))
    if (str (time1) not in str (time2)):

        try:
            create_query = " UPDATE " + classes_names.tasks + " set updated = to_timestamp(CAST (%s AS bigint)/1000)," \
                                                              "closed=to_timestamp(CAST (%s AS bigint)/1000)," \
                                                              " status=%s where id = (%s) ;"
            cur.execute (create_query, (updated, closed, status, id,))
            con.commit ()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while updating tasks  PostgreSQL table LINE : ", error)

def close_task(con, cur, id):
    try:
        query = " SELECT closed from " + classes_names.tasks + " where id =%s ;"
        cur.execute (query, (id,))
        query_result = cur.fetchall ()
        if (query_result[0][0] == None):
            create_query = " UPDATE  " + classes_names.tasks + " set status =%s," \
                                                               "closed=%s where id = (%s) ;"
            cur.execute (create_query, ("closed", datetime.now (tz=timezone ('Europe/Budapest')), id,))
            con.commit ()
            print ("local task is closed ID = ", id)
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Error while closing  tasks  PostgreSQL table LINE : ", error)


class Task:
    def __init__(self, id, project_id, employee_id, name, created, updated, closed, status, metadata):
        self.id = id
        self.project_id = project_id
        self.employee_id = employee_id
        self.name = name
        self.created = created
        self.updated = updated
        self.closed = closed
        self.status = status
        self.metadata = metadata

    def insert_into_db(self, connection, cursor):
        try:
            query = "INSERT INTO " + classes_names.tasks + "(project_id,employee_id," \
                                                           "name,created,updated,closed," \
                                                           "status,metadata)VALUES(%s,%s,%s," \
                                                           " to_timestamp(CAST (%s AS bigint)/1000)," \
                                                           " to_timestamp(CAST (%s AS bigint)/1000)," \
                                                           " to_timestamp(CAST (%s AS bigint)/1000),%s,%s)" \
                                                           " RETURNING id;"
            cursor.execute (query, (self.project_id, self.employee_id, self.name,
                                    self.created, self.updated, self.closed, self.status, json.dumps(self.metadata),))
            connection.commit ()
            query_result = cursor.fetchone ()
            return query_result[0]
        except (Exception, psycopg2.DatabaseError) as error:
            raise NameError ('failed to insert the Task record ', error)
