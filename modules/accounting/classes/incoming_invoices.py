import psycopg2
from configuration import classes_names
import json
create_table_query = "CREATE TABLE "+classes_names.incoming_invoices+"" \
                     "(local_id SERIAL PRIMARY KEY  NOT NULL," \
                     "title varchar ,invoice_id int,created_date date ,expiration_date date,fullfillement_date date ," \
                     "total_amount double precision , total_vat double precision," \
                     "currency varchar ,products json,status varchar); "
def getById(connnection, cursor, id):
    try:

        query = " SELECT * from " + classes_names.incoming_invoices + " where local_id=%s ;"
        cursor.execute (query, id, )
        query_result = cursor.fetchall ()
        if (len (query_result) != 0):

            if (len (query_result) != 0):
                if (query_result[0][3] != None):
                    created_date = str (query_result[0][3])
                else:
                    created_date = query_result[0][3]

                if (query_result[0][4] != None):
                    expiration_date = str (query_result[0][4])
                else:
                    expiration_date = query_result[0][4]
                if (query_result[0][5] != None):
                    fullfillement_date = str (query_result[0][5])
                else:
                    fullfillement_date = query_result[0][5]
            invoice = \
                {"ID": query_result[0][0],
                 "title ": query_result[0][1],
                 "invoice_id":query_result[0][2],
                 "created_date": created_date,
                  "expiration_date": expiration_date,
                  "fullfillement_date": fullfillement_date,
                 "total_amount": query_result[0][6],
                 "total_vat": query_result[0][7],
                 "currency": query_result[0][8],
                 "products": query_result[0][9],
                 "status": query_result[0][10]
                 }
            return json.dumps (invoice)
        else:
            return []

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during get By ID function , ERROR : ", error)
def getAll(connnection, cursor):
    try:

        query = " SELECT * from " + classes_names.incoming_invoices + " ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        invoices = []
        if (len (query_result) != 0):

            for x in range (len (query_result)):

                    if (query_result[x][3] != None):
                        created_date = str (query_result[x][3])
                    else:
                        created_date = query_result[x][3]

                    if (query_result[x][4] != None):
                        expiration_date = str (query_result[x][4])
                    else:
                        expiration_date = query_result[x][4]
                    if (query_result[x][5] != None):
                        fullfillement_date = str (query_result[x][5])
                    else:
                        fullfillement_date = query_result[x][5]
                    invoice = \
                    {"ID": query_result[x][0],
                     "title ": query_result[x][1],
                     "invoice_id": query_result[x][2],
                     "created_date": created_date,
                     "expiration_date": expiration_date,
                     "fullfillement_date": fullfillement_date,
                     "total_amount": query_result[x][6],
                     "total_vat": query_result[x][7],
                     "currency": query_result[x][8],
                     "products": query_result[x][9],
                     "status": query_result[x][10]
                     }

                    invoices.append (invoice)

        Result_json = {"invoices": invoices}
        return json.dumps (Result_json)


    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during getAll function , ERROR : ", error)
def InsertInvoice(connnection,cursor,title,invoice_id,created_date,expiration_date,fullfillement_date
                    ,total_amount,total_vat,currency,products,status):
    try:
        query = "INSERT INTO "+classes_names.incoming_invoices+" (title,invoice_id,created_date,expiration_date,fullfillement_date," \
                    "total_amount,total_vat,currency,products,status)" \
         "           VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s );"
        cursor.execute (query,(title,invoice_id,created_date,expiration_date,fullfillement_date
                    ,total_amount,total_vat,currency,products,status,))
        connnection.commit ()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception during inserting into incoming_invoices table , ERROR : ", error)

def GetAllIncomingInvoices(connection,cursor):
    try:
        var=[]
        query=" SELECT invoice_id from "+classes_names.incoming_invoices+" ;"
        cursor.execute (query)
        query_result = cursor.fetchall ()
        if (len(query_result)!=0):
            for x in range(len(query_result)):
                var.append ( int(query_result[x][0]))
        return var
    except:
        print("Exception during GetAllOutgoingInvoices Function ")

def update_quickbooks (connection,cursor,invoice_id,balance):
    try:

        query = " SELECT status from " + classes_names.incoming_invoices + " where invoice_id =%s ;"
        cursor.execute (query,(invoice_id,))
        query_result = cursor.fetchall ()
        if (len(query_result)!=0):

            if(balance == 0.0 and query_result[0][0]!="PAID"):
                try:
                    create_query = " UPDATE " + classes_names.incoming_invoices + " set status = %s "\
                                                               " where invoice_id = (%s) ;"
                    cursor.execute (create_query, ( "PAID", invoice_id,))
                    connection.commit ()
                except (Exception, psycopg2.DatabaseError) as error:
                    print ("Error while updating outgoing invoice status  : ", error)
    except:
        print ("Exception during update outgoing invoice  Function ")
def update(connection,cursor,invoice_id,status):
    try:

        query = " SELECT status from " + classes_names.incoming_invoices + " where invoice_id =%s ;"
        cursor.execute (query,(invoice_id,))
        query_result = cursor.fetchall ()
        if (len(query_result)!=0):
            create_query = " UPDATE " + classes_names.incoming_invoices + " set status = %s " \
                                                                         " where invoice_id = (%s) ;"

            if(query_result[0][0]!="NOT PAID" and status== True):
                print(" invoice Status from :NOT PAID to PAID ")
                prompt=" 1:Update the ERP database | anything else :Do not update the ERP database "
                userInp = ""
                userInp = input (prompt)
                if userInp == '1':
                    try:
                        cursor.execute (create_query, ( "PAID", invoice_id,))
                        connection.commit ()
                    except (Exception, psycopg2.DatabaseError) as error:
                        print ("Error while updating incoming invoice status  : ", error)
                else:
                    None

            else:

                if (query_result[0][0] == "PAID" and status == False):
                    print (" invoice Status from :PAID to NOT PAID ")
                    prompt = " 1:Update the ERP database | anything else :Do not update the ERP database "
                    userInp = ""
                    userInp = input (prompt)
                    if userInp == '1':
                        try:
                            cursor.execute (create_query, ("NOT PAID", invoice_id,))
                            connection.commit ()
                        except (Exception, psycopg2.DatabaseError) as error:
                            print ("Error while updating incoming invoice status  : ", error)
                else:
                    None
    except:
        print ("Exception during update incoming invoice  Function ")