from configuration import classes_names
def create_table() :
    create_table_query = "CREATE TABLE "+classes_names.incoming_invoices+"" \
                     "(local_id SERIAL PRIMARY KEY  NOT NULL," \
                     "title varchar ,invoice_id int,created_date date ,expiration_date date,fulfillment_date date ," \
                     "total_amount double precision , total_vat double precision," \
                     "currency varchar ,products json,status varchar); "
    return create_table_query

class Invoice:
    def __init__(self,id,title,invoice_id,created,expiration_date,fulfillment_date,total_amount,total_vat,
                 currency,products,status):
        self.id=id
        self.title=title
        self. invoice_id=invoice_id
        self. created=created
        self. expiration_date=expiration_date
        self. fullfillement_date=fulfillment_date
        self.total_amount =total_amount
        self. total_vat=total_vat
        self.currency =currency
        self.products =products
        self. status=status




