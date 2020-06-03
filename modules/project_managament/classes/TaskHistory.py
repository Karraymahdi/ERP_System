from configuration import classes_names


def create_table():
    create_table_query = "CREATE TABLE " + classes_names.task_history + "" \
    " (task_id integer REFERENCES " + classes_names.tasks + "(id)," \
                                                       " old_updated TIMESTAMP," \
                                                       " new_updated TIMESTAMP ," \
                                                       " from_status varchar ," \
                                                       " to_status varchar," \
                                                       " closed varchar ); "
    return create_table_query

create_trigger_update= "CREATE TRIGGER HisUpdate" \
                " AFTER UPDATE ON "+classes_names.tasks+"" \
                " FOR EACH ROW  EXECUTE PROCEDURE aft_update(); "


procedure_update="CREATE OR REPLACE FUNCTION aft_update()" \
          " RETURNS trigger AS $HisUpdate$ " \
          " BEGIN " \
          " INSERT into " +classes_names.task_history+ " (task_id,old_updated,new_updated,from_status,to_status,closed)" \
          " VALUES (NEW.id,OLD.updated,NEW.updated,OLD.status,NEW.status,NEW.closed);" \
          "RETURN NEW;" \
          "END;" \
          "$HisUpdate$ LANGUAGE plpgsql; "


create_trigger_insert= "CREATE TRIGGER HisInsert" \
                " AFTER INSERT ON "+classes_names.tasks+"" \
                " FOR EACH ROW  EXECUTE PROCEDURE aft_Insert(); "

procedure_insert="CREATE OR REPLACE FUNCTION aft_Insert()" \
          " RETURNS trigger AS $HisInsert$ " \
          " BEGIN " \
          " INSERT into " +classes_names.task_history+ " (task_id,old_updated,new_updated,from_status,to_status,closed)" \
          " VALUES (NEW.id,NULL,NEW.updated,NULL,NEW.status,NEW.closed);" \
          "RETURN NEW;" \
          "END;" \
          "$HisInsert$ LANGUAGE plpgsql; "

class TaskHistory:
    def __init__(self,id,old_updated,new_updated,old_status,new_status,closed):
        self.id=id
        self.old_updated =old_updated
        self. new_updated=new_updated
        self.old_status =old_status
        self. new_status=new_status
        self.closed =closed







