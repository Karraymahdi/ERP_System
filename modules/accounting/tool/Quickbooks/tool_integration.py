from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.invoice import Invoice
from configuration import classes_names, tools_keys, database_setting as db_set
from quickbooks.objects.bill import Bill
from database import Database, methods
from modules.accounting.classes import outgoing_invoices,incoming_invoices

import json
auth_client = AuthClient(
        client_id=tools_keys.client_id,
        client_secret=tools_keys.client_secret,
        environment='sandbox',
        redirect_uri=tools_keys.redirect_uri,
    )
client = QuickBooks (
    auth_client=auth_client,
    refresh_token=tools_keys.refresh_token,
    company_id=tools_keys.company_id,
)

#---------------------------------------connect to database----------------------------------------

try:#try to connect to the database

    db = Database.Database (db_set.database, db_set.user, db_set.password, db_set.host, db_set.port)
    try:
        con = db.connection ()
        con.autocommit = True
        cur = con.cursor ()
        print ("database ", db.name, "is opened")
    except:
        raise NameError ('failed to open the database')

#---------------------- outgoing_Invoices----------------------
    try:

        LocalInvoicesIDs=outgoing_invoices.GetAllOutgoingInvoices(con,cur)
        invoices=Invoice.all(qb=client)
        for x in range (len (invoices)):
            invoice_id = int(invoices[x].Id)
            if(invoice_id  not in LocalInvoicesIDs ):

                title=invoices[x].CustomerRef.name
                created_date=invoices[x].TxnDate
                expiration_date=invoices[x].DueDate
                fullfillement_date=None
                total_amount=invoices[x].TotalAmt
                total_vat=invoices[x].TxnTaxDetail.TotalTax
                currency=invoices[x].CurrencyRef.value
                products_list=[]
                list_products= (invoices[x].Line)
                for y in range(len(list_products)):
                    try:
                        Description=list_products[y].Description
                    except:
                        Description="NULL"
                    try:
                        DetailType = list_products[y].DetailType
                    except:
                        DetailType = "NULL"
                    try:
                        Qty = list_products[y].SalesItemLineDetail.Qty
                    except:
                        Qty = "NULL"
                    try:
                        UnitPrice = list_products[y].SalesItemLineDetail.UnitPrice
                    except:
                        UnitPrice = "NULL"
                    try:
                        Amount = list_products[y].Amount
                    except:
                        Amount = "NULL"
                    product={"Description":Description,
                             "DetailType":DetailType,
                             "Qty":Qty,
                             "UnitPrice":UnitPrice,
                             "Amount":Amount}
                    products_list.append(product)

                products = json.dumps({"products": products_list})
                if(invoices[x].Balance!=0):
                    status="NOT PAID"
                else:
                    status = "PAID"
                outgoing_invoices.InsertInvoice(con,cur,title,invoice_id,created_date,expiration_date,fullfillement_date,
                                                total_amount,total_vat,currency,products,status)
            else:

                outgoing_invoices.update(con,cur,invoice_id,invoices[x].Balance)
    except:
        print("problem when getting invoice from quickbook")
# ---------------------- incoming_Invoices----------------------
    try:

        LocalInvoicesIDs = incoming_invoices.GetAllIncomingInvoices(con, cur)
        invoices = Bill.all (qb=client)
        for x in range (len (invoices)):
            invoice_id = int (invoices[x].Id)
            if (invoice_id not in LocalInvoicesIDs):
                title = invoices[x].VendorRef.name
                created_date = invoices[x].TxnDate
                expiration_date = invoices[x].DueDate
                fullfillement_date = None
                total_amount = invoices[x].TotalAmt
                total_vat = None
                currency = invoices[x].CurrencyRef.value
                products_list = []
                list_products = (invoices[x].Line)
                for y in range (len (list_products)):
                    try:
                        Description = list_products[y].Description
                    except:
                        Description = "NULL"

                    product = {"Description": Description}
                    products_list.append (product)

                products = json.dumps ({"products": products_list})
                if (invoices[x].Balance != 0):
                    status = "NOT PAID"
                else:
                    status = "PAID"
                incoming_invoices.InsertInvoice (con, cur, title, invoice_id, created_date, expiration_date, fullfillement_date,
                                                 total_amount, total_vat, currency, products, status)
            else:

                incoming_invoices.update (con, cur, invoice_id, invoices[x].Balance)
    except:
        print ("problem when getting invoice from quickbook")
except:
    None
