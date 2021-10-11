import mysql.connector
from mysql.connector.errors import Error





def connnection ():
    try:
        mydb = mysql.connector.connect(
        host= "localhost",
        user= "admin",
        password= "123456789",
        database= "medicamentos_imss"
        )
        return mydb
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))    

def CargarDatos():
    mydb =connnection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Medicamentos")
    myresult = mycursor.fetchall()
    return myresult
    



