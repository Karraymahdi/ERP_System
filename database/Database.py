import psycopg2
class Database:
    def __init__(self,name, user, password,host,port):
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def check(self): # check if the database exist or not
        try:
            con = psycopg2.connect(database=self.name, user=self.user, password=self.password,
                                   host=self.host, port=self.port)
            print("Database " ,self.name,"exist")
            con.close()
            return True #try to connect to the database to check if it exist
        except:
            return False# database doesn't exist

    def create(self): # create the database
        try:
            connection = psycopg2.connect (database="", user=self.user, password=self.password,
                                    host=self.host, port=self.port)
            connection.autocommit = True
            cursor = connection.cursor ()
            cursor.execute ('CREATE DATABASE {};'.format (self.name))
            print (" Database is created successfully")
            connection.close ()
        except(Exception, psycopg2.DatabaseError) as error:
             print ("Error while creating the database | Error : ", error)

    def connection(self):
        try:
            connection = psycopg2.connect (database=self.name, user=self.user, password=self.password,
                                    host=self.host, port=self.port)
            print ("Database opened successfully")
            return connection
        except:
            print ("failed to open the database ")
            return None




