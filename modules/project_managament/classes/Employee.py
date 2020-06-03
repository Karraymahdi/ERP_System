from configuration import classes_names
import psycopg2
def create_table():
    create_table_query = "CREATE TABLE " + classes_names.employee + "" \
                                                                    "(id SERIAL PRIMARY KEY     NOT NULL," \
                                                                    "name varchar ," \
                                                                    "birth_date date , " \
                                                                    "mother_name varchar ," \
                                                                    "personal_id varchar ," \
                                                                    "card_id varchar ," \
                                                                    "status varchar ," \
                                                                    "country varchar ," \
                                                                    "city varchar ," \
                                                                    "zip integer ," \
                                                                    "address varchar ," \
                                                                    "place_of_birth varchar ," \
                                                                    "tax_number integer ," \
                                                                    "social_security_number integer," \
                                                                    "bank_account varchar," \
                                                                    "email varchar ," \
                                                                    "phone_number integer ," \
                                                                    "first_day_of_work date ," \
                                                                    "job_title varchar ," \
                                                                    "is_external boolean," \
                                                                    "number_of_children  int ," \
                                                                    "manager_id int ," \
                                                                    "hours_per_day double precision); "
    return create_table_query
def get_id_by_name(cursor,name):
    try:
        query = " SELECT id from "+classes_names.employee+\
                " where UPPER(NAME)= upper(%s) ;"
        cursor.execute (query, (name,))
        query_result = cursor.fetchone()
        if (query_result == None):
            return []
        return query_result
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Exception appers while calling get_id_by_name method , ERROR :  ", error)

class Employee:
    def __init__(self,id,name,birth_date,mother_name,
                   personal_id,card_id,status,country,
                   city,zip,address,place_of_birth,
                   tax_number,social_security_number,bank_account,
                   email,Phone_number,first_day_of_work,
                   job_title,is_external,number_of_children,
                   manager_id,hours_per_day):

        self.id=id
        self.name=name
        self.birth_date=birth_date
        self.mother_name=mother_name
        self.personal_id=personal_id
        self.card_id=card_id
        self.status =status
        self.country =country
        self.city =city
        self.zip=zip
        self.address =address
        self.place_of_birth =place_of_birth
        self.tax_number =tax_number
        self.social_security_number =social_security_number
        self.bank_account =bank_account
        self.email =email
        self.Phone_number =Phone_number
        self. first_day_of_work=first_day_of_work
        self.job_title =job_title
        self.is_external =is_external
        self.number_of_children =number_of_children
        self.manager_id =manager_id
        self.hours_per_day =hours_per_day

