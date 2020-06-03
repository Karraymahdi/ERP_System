import psycopg2
from configuration import classes_names
import json
def create_table():
    create_table_query = "CREATE TABLE "+classes_names.cash_flow+"" \
                     "(id SERIAL PRIMARY KEY     NOT NULL," \
                     "title varchar ,date date , " \
                     "total_amount double precision," \
                     "currency varchar ,products json); "
    return create_table_query

def InsertCash_transaction(connnection,cursor,title,date,total_amount,currency,products ):
    try:
        query = "INSERT INTO "+classes_names.cash_flow+" (title,date,total_amount,currency,products" \
                    "           VALUES(%s,%s,%s,%s,%s);"
        cursor.execute (query,(title,date,total_amount,currency,products,))
        connnection.commit ()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during inserting into cash_flow table , ERROR : ", error)


def getById(connnection, cursor,id):
    try:

        query = " SELECT * from " + classes_names.cash_flow + " where local_id=%s ;"
        cursor.execute (query,id,)
        query_result = cursor.fetchall ()
        if (len (query_result)!=0) :

                if (query_result[0][2] != None):
                    date = str (query_result[0][2])
                else:
                    date = query_result[0][2]
                transaction=\
                    {"ID": query_result[0][0],
                     "title ": query_result[0][1],
                     "date":date,
                     "total_amount":query_result[0][3],
                     "currency":(query_result[0][4]),
                     "products":(query_result[0][5])}
                return json.dumps(transaction)
        else: return  []

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during get By ID function , ERROR : ", error)

def getAll(connnection, cursor):
    try:
        query = " SELECT * from " + classes_names.cash_flow + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        transactions = []
        if (len (query_result)!=0) :

            for x in range(len (query_result)):
                if (query_result[x][2] != None):
                    date = str (query_result[x][2])
                else:
                    date = query_result[x][2]
                transaction = \
                    {"ID": query_result[x][0],
                     "title ": query_result[x][1],
                     "date": date,
                     "total_amount": query_result[x][3],
                     "currency": (query_result[x][4]),
                     "products": (query_result[x][5])}
                transactions.append(transaction)
        Result_json = {"cash_transactions": transactions}
        return json.dumps(Result_json)

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)
