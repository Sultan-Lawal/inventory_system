import mysql.connector
from mysql.connector import Error
import db

def connect_database():

    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "inventory_db"
        )

        if mydb.is_connected():
            return mydb

    except Error as e:
        print("Database Connection Error:",e)
        return None


def low_stock_report(quantity):
        
    try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        mycursor.execute("SELECT product_name, quantity FROM products WHERE quantity < %s", (quantity,))

        record = mycursor.fetchall()

        if len(record) == 0:
            print("No Low Stock!")

        return record

    except Error as e:
        print(e)

        return []

def daily_sales_report():
    try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        sql = """SELECT SUM(s.quantity_sold), SUM(s.total_amount),
            SUM((s.total_amount - p.cost_price * s.quantity_sold)) 
            FROM sales s JOIN products p ON s.product_id = p.product_id
            WHERE DATE(s.sale_date) = CURDATE()"""    

        mycursor.execute(sql)

        totals = mycursor.fetchone()

        if totals[0] is None:
            print("No Sales Today!")   
            return None, []     

        query = """ SELECT p.product_name, SUM(s.quantity_sold), SUM(s.total_amount),
            SUM((s.total_amount - p.cost_price * s.quantity_sold)) FROM sales s JOIN products p
            ON s.product_id = p.product_id WHERE DATE(s.sale_date) = CURDATE()
            GROUP BY p.product_name 
            """    

        
        mycursor.execute(query)

        breakdown = mycursor.fetchall()

        return totals, breakdown

    except Error as e:
        print(e)

        return None, []