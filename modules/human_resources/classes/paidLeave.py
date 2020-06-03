from configuration import classes_names
def create_table():
    create_table_query = "CREATE TABLE "+classes_names.paid_leave+"" \
                     "(id  SERIAL PRIMARY KEY  NOT NULL," \
                     "employee_id integer REFERENCES "+classes_names.employee+"(id)," \
                     "start_day_id integer REFERENCES  "+classes_names.calendar+"(id),                  " \
                     "end_day_id integer REFERENCES  "+classes_names.calendar+"(id)                         );"
    return create_table_query


