from modules.accounting.tool.kashoo import Kashoo_api
from modules.accounting.classes import incoming_invoices
from configuration import database_setting as db_set
from database import Database
from datetime import datetime
if __name__ == '__main__':

    db = Database.Database (db_set.database, db_set.user, db_set.password, db_set.host, db_set.port)
    try:
        connection = db.connection ()
        connection.autocommit = True
        cursor = connection.cursor ()
        print ("database ", db.name, "is opened")
    except:
        raise NameError ('failed to open the database')

    try:
        LocalInvoicesIDs = incoming_invoices.GetAllIncomingInvoices(connection, cursor)
        bills = Kashoo_api.get_all_bills()
        for x in range (len (bills)):
            invoice_id = int (bills[x]["number"])
            if (invoice_id not in LocalInvoicesIDs):
                title = bills[x]["contactName"]
                created_date = datetime.fromtimestamp ((bills[x]["creation"]) / 1000)
                expiration_date = bills[x]["dueDate"]
                fullfillement_date = None
                total_amount = bills[x]["totalDue"]/100
                taxes = bills[x]["taxes"]
                total_vat = 0
                for y in range (len (taxes)):
                    total_vat = total_vat + taxes[y]["amount"] / 100
                currency = bills[x]["currency"]
                products_list = []
                if (bills[x]["paid"]!= True):
                    status = "NOT PAID"
                else:
                    status = "PAID"
                incoming_invoices.InsertInvoice (connection, cursor, title, invoice_id, created_date, expiration_date, fullfillement_date,
                                                 total_amount, total_vat, currency, products_list, status)
            else:

                incoming_invoices.update (connection, cursor, invoice_id,bills[x]["paid"] )
    except:
        print ("Exception during update outgoing invoice  Function ")

