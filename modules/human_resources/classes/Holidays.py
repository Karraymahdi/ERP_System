from configuration import classes_names
def create_table():
    create_table_query = "CREATE TABLE holiday                       " \
                     "(id  SERIAL PRIMARY KEY  NOT NULL," \
                     " calendarlocalID int REFERENCES  calendar(id)); "
    return create_table_query
