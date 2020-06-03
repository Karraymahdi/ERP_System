from bottle import *
import requests
from Tables.hr import recruitment,Project_Progress
from Tables.ProjectManagement import projects,employee,tasks,Spaces
from Tables.tools import tools
from Tables.Accounting import incoming_invoices,outgoing_invoices,payroll,grants,cash_flow
from DatabaseConnection import database_connection

#---------------HR API----------------------
@route('/hr/recruitment',method='GET')
def getAll():
    return (recruitment.getAll(con,cur))
@route('/hr/recruitment/<id>',method='GET')
def getById(id):
    return (recruitment.getById(con,cur,id))
@route('/hr/progress',method='GET')
def getAll():
    return (Project_Progress.getAll(con,cur))
@route('/hr/progress/<id>',method='GET')
def getById(id):
    return (Project_Progress.getById(con,cur,id))

#---------ProjectManagement API------------------
@route('/tools',method='GET')
def getAll():
    return (tools.getAll(con,cur))
@route('/tools/<id>',method='GET')
def getById(id):
    return (tools.getById(con,cur,id))
@route('/spaces',method='GET')
def getAll():
    return (Spaces.getAll(con,cur))
@route('/spaces/<id>',method='GET')
def getById(id):
    return (Spaces.getById(con,cur,id))
@route('/projects',method='GET')
def getAll():
    return (projects.getAll(con,cur))
@route('/projects/<id>',method='GET')
def getById(id):
    return (projects.getById(con,cur,id))
@route('/tasks',method='GET')
def getAll():
    return (tasks.getAll(con,cur))
@route('/tasks/<id>',method='GET')
def getById(id):
    return (tasks.getById(con,cur,id))
@route('/employee',method='GET')
def getAll():
    return (employee.getAll(con,cur))
@route('/employee/<id>',method='GET')
def getById(id):
    return (employee.getById(con,cur,id))
@route('/employee',method='POST')
def insert_employee():
    name = request.forms.get ('name', None)
    dof= request.forms.get ('dof', None)
    mothername = request.forms.get ('motherName', None)
    personalid = request.forms.get ('personalID', None)
    cardid = request.forms.get ('cardID', None)
    status = request.forms.get ('status', None)
    country = request.forms.get ('country', None)
    city = request.forms.get ('city', None)
    zip = request.forms.get ('zip', None)
    address = request.forms.get ('address', None)
    placeofbirth = request.forms.get ('placeOfBirth', None)
    taxNumber = request.forms.get ('taxNumber', None)
    socialsecurityNumber = request.forms.get ('socialSecurityNumber', None)
    bankaccount = request.forms.get ('bankAccount', None)
    email = request.forms.get ('email', None)
    PhoneNumber = request.forms.get ('PhoneNumber', None)
    firstdayofwork = request.forms.get ('firstDayOfwork', None)
    jobtitle = request.forms.get ('jobTitle', None)
    isexternal=request.forms.get ('isExternal', None)
    Numberofchildren = request.forms.get ('NumberOfchildren', None)
    superiorEmployeeID = request.forms.get ('superiorEmployeeID', None)
    hoursperday=request.forms.get ('hoursperday', None)

    return employee.InsertEmployee(con,cur, name, dof, mothername,
                                    personalid,
                                    cardid, status,
                                    country, city, zip, address, placeofbirth,
                                    taxNumber, socialsecurityNumber, bankaccount,
                                    email, PhoneNumber, firstdayofwork,
                                    jobtitle, isexternal, Numberofchildren,
                                    superiorEmployeeID, hoursperday)

#---------accounting API------------------
@route('/invoices/incoming/<id>',method='GET')
def getById(id):
    return (incoming_invoices.getById(con,cur,id))
@route('/invoices/incoming',method='GET')
def getAll():
    return (incoming_invoices.getAll(con,cur))
@route('/invoices/outgoing/<id>',method='GET')
def getById(id):
    return (outgoing_invoices.getById(con,cur,id))
@route('/invoices/outgoing',method='GET')
def getAll():
    return (outgoing_invoices.getAll(con,cur))
@route('/grants/<id>',method='GET')
def getById(id):
    return (grants.getById(con,cur,id))
@route('/grants',method='GET')
def getAll():
    return (grants.getAll(con,cur))
@route('/payroll/<id>',method='GET')
def getById(id):
    return (payroll.getById(con,cur,id))
@route('/payroll',method='GET')
def getAll():
    return (payroll.getAll(con,cur))
@route('/cash/<id>',method='GET')
def getById(id):
    return (cash_flow.getById(con,cur,id))
@route('/cash',method='GET')
def getAll():
    return (cash_flow.getAll(con,cur))

if __name__=='__main__':

    try:
        con = database_connection.connection ()
        cur = con.cursor ()
        run (host='localhost', port=8080, debug=True)
    except:
        print ("fail to open the database")

