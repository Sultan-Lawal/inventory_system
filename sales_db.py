import mysql.connector
from mysql.connector import Error

def connect_database():
    
    try:

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "inventory_db"
        )

        if mydb.is_connected():
            # print("Database Connected!")
            return mydb

    except Error as e: 
        print(f"Error: {e}")
        return None    

    sql = """  CREATE TABLE sales (
      sale_id INT AUTO_INCREMENT,
      product_id INT,
      quantity_sold INT,
      unit_price DECIMAL(10,2),
      total_amount DECIMAL(10,2),
      sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(sale_id)
      )"""

    mycursor = mydb.cursor()
    mycursor.execute(sql)

def record_sale(product_id, quantity, unit_price, total_amount):

    try: 
        mydb = connect_database()

        if mydb:
            mycursor = mydb.cursor()

            mycursor.execute("SELECT quantity FROM products WHERE product_id = %s", (product_id,))

            record = mycursor.fetchone()

            if record[0] >= quantity:
                sql = """ INSERT INTO sales(product_id, quantity_sold, unit_price, total_amount)
                    VALUES (%s, %s, %s, %s)
                    """
                values = (product_id, quantity, unit_price, total_amount)
                
                mycursor.execute(sql, values)
                
                mydb.commit()
                
                
                query = """UPDATE products 
                    SET quantity = quantity - %s
                    WHERE product_id = %s
                    """

                vl = (quantity, product_id)

                mycursor.execute(query, vl)

                mydb.commit()

                return True
                
            else:
                print("Not enough stock: only",record[0],"available.")
            


            

    except Error as e:
        print(f"Error: {e}")

        return None, []

    finally:
        if mydb.is_connected():

            mycursor.close()

            mydb.close()

def view_sales():

    try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM sales")

        record = mycursor.fetchall()

        return record

    except Error as e:

        print(e)

        return []

    finally:
        if mydb.is_connected():
            
            mycursor.close()

            mydb.close()





                



