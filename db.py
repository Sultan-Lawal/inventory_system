import mysql.connector 
from mysql.connector import Error

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "inventory_db"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE inventory_db")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "inventory_db"
        )
        
        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)
        return None
