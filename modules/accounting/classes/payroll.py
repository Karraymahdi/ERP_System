import psycopg2
from configuration import classes_names
import json
create_table_query = "CREATE TABLE "+classes_names.payroll+"" \
                     "(local_id SERIAL PRIMARY KEY     NOT NULL," \
                     "employeeID integer REFERENCES "+classes_names.employee+"(id),payment_date date, " \
                     "total_amount double precision," \
                      "currency varchar ); "

def InsertPayroll_transaction(connnection,cursor,employeeID,payment_date,total_amount,currency):
    try:
        query = "INSERT INTO "+classes_names.payroll+" (employeeID,payment_date,total_amount,currency" \
                    "           VALUES(%s,%s,%s,%s);"
        cursor.execute (query,(employeeID,payment_date,total_amount,currency,))
        connnection.commit ()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during inserting into payroll table , ERROR : ", error)


def getById(connnection, cursor, id):
    try:

        query = " SELECT * from " + classes_names.payroll + " where local_id=%s ;"
        cursor.execute (query, id, )
        query_result = cursor.fetchall ()
        if (len (query_result) != 0):

            if (query_result[0][2] != None):
                date = str (query_result[0][2])
            else:
                date = query_result[0][2]
            transaction = \
                {"ID": query_result[0][0],
                 "employeeID ": query_result[0][1],
                 "payment_date": date,
                 "total_amount": query_result[0][3],
                 "currency": (query_result[0][4])}
            return json.dumps (transaction)
        else:
            return []


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during get By ID function , ERROR : ", error)


def getAll(connnection, cursor):
    try:

        query = " SELECT * from " + classes_names.payroll + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        transactions = []
        if (len (query_result) != 0):

            for x in range (len (query_result)):
                if (query_result[x][2] != None):
                    date = str (query_result[x][2])
                else:
                    date = query_result[x][2]
                transaction = \
                    {"ID": query_result[x][0],
                     "employeeID ": query_result[x][1],
                     "payment_date": date,
                     "total_amount": query_result[x][3],
                     "currency": (query_result[x][4])}
                transactions.append (transaction)

        Result_json = {"payroll": transactions}
        return json.dumps (Result_json)


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)
