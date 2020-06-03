import psycopg2
from configuration import classes_names
import json
from datetime import datetime


def create_table():
    create_table_query = "CREATE TABLE " \
                         + classes_names.projects + "" \
                                                    "(id SERIAL PRIMARY KEY NOT NULL," \
                                                    "space_id INTEGER REFERENCES " \
                         + classes_names.spaces + "(id)," \
                                                  "name VARCHAR  NOT NULL," \
                                                  "tool_project_id INTEGER ," \
                                                  "created TIMESTAMP ," \
                                                  "archived BOOLEAN ," \
                                                  "metadata JSON ); "
    return create_table_query
class Project:
    def __init__(self, id, space_id, name, tool_project_id, created, archived, metadata):
        self.id = id
        self.space_id = space_id
        self.name = name
        self.tool_project_id = tool_project_id
        self.created = created
        self.archived = archived
        self.metadata = metadata

    def insert_into_db(self, connection, cursor):
        try:
            query = "INSERT INTO " + classes_names.projects + " (space_id, name, tool_project_id, created, archived, metadata)" \
                                                       "        VALUES(%s,%s,%s,CURRENT_TIMESTAMP,FALSE,%s )RETURNING id;"
            cursor.execute (query, (self.space_id, self.name,self.tool_project_id, self.metadata,))
            connection.commit ()
            query_result = cursor.fetchone ()
            return query_result[0]
        except (Exception, psycopg2.DatabaseError) as error:
            raise NameError ('failed to insert the space record ', error)
            print ("Exception during inserting into space table , ERROR : ", error)

    def get_id(self):
        return self.id
    def get_space_id(self):
        return self.space_id
    def set_space_id(self,space_id):
        self.space_id=space_id
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name=name
    def get_created(self):
        return self.created
    def get_archived(self):
        return self.archived
    def set_archived(self,archived):
        self.archived=archived
    def get_metadata(self):
        return self.metadata
    def set_metadata(self,metadata):
        self.metadata=metadata



