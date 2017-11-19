import pymysql
import ssdeep
hostname= '54.153.14.97'
username='ubuntu'
password='insure'
database='hashdb'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT fname, lname FROM employee" )
    for firstname, lastname in cur.fetchall() :
        print firstname, lastname

myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
doQuery( myConnection )
myConnection.close()
