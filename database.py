##############################################
## Authors: Dorian HENAULT and Alexis SEGURA##
## Email: alex.segura06@gmail.com ############
## Status: In development #################### 
## Version: 0.1 ##############################
##############################################

import pymysql
import json

with open('credentials.json', 'r') as f:
    credentials = json.load(f)
    
###### Example of method calls ######
'''
database.connectDB()
database.insertData("ending_status",{"id":"2","label":"KO"})
database.readData("ending_status",["*"])
database.disconnectDB()

'''

###### Open database connection ######
def connectDB(): 
    global db
    db = pymysql.connect(credentials["database"]["host"],credentials["database"]["username"],credentials["database"]["password"],credentials["database"]["dbname"])

###### disconnect from server ######    
def disconnectDB():
    db.close()




###### Insert data into a table ######
'''
table is the name of the table(string) and data is a dictionnary :
the key is the attribute and the value is the attributes' value
'''
def insertData(table,data):
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    attrib = "";
    value = "";
    for attr in data.keys():
        attrib += attr+","
    attrib=attrib[:-1]

    for dat in data.values():
        value += "'"+dat+"',"
    value=value[:-1]
    
    sql = "INSERT INTO "+table+"("+attrib+") VALUES ("+value+")"
    print(sql)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
       print("error")


###### Read data from a table ######
'''
table is the name of the table(string) and attribute is a list containing
the attributes to retrieve
'''
def readData(table,attributes):
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    attr=""
    for att in attributes:
        attr+=att+","
    attr=attr[:-1]
    # Prepare SQL query to READ a record into the database.
    sql = "SELECT "+attr+" FROM "+table
    print(sql)
    try:
       # Execute the SQL command
        cursor.execute(sql)
       # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        resultStr=""
        for row in results:
            for i in range(0,len(row)):
                resultStr+=str(row[i])+", "
            resultStr+="\n"
        print (resultStr[:-3])
    except:
        print ("Error: unable to fetch data")

   


