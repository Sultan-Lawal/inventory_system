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
          print("Database Connection Error:",e)
          return None     

     sql = """  CREATE TABLE products (
        product_id INT AUTO_INCREMENT,
        product_name VARCHAR(100),
        category VARCHAR(50),
        quantity INT,
        cost_price DECIMAL(10,2),
        selling_price DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(product_id)
        )"""

     mycursor = mydb.cursor()
     mycursor.execute(sql)

def add_product(product_name, category, quantity, cost_price, selling_price):

     try:
        mydb = connect_database()

        if mydb:
          mycursor = mydb.cursor()


          sql = """ INSERT INTO products(product_name, category, quantity, cost_price, selling_price)
          VALUES (%s, %s, %s, %s, %s)
          """
          values = (product_name, category, quantity, cost_price, selling_price)

          mycursor.execute(sql, values)

          mydb.commit()

          print("Product added sucessfully!")

     except Error as e:
        print(f"Error: {e}")      

     finally:
         if mydb.is_connected():
             
          mycursor.close()

          mydb.close()

def view_product():
     try:
          mydb = connect_database()

          mycursor = mydb.cursor()

          mycursor.execute("SELECT * FROM products")

          record = mycursor.fetchall()

          return record

     except Error as e:
          print(e)

          return []

     finally:

          if mydb.is_connected():
                  
               mycursor.close()
     
               mydb.close()



def update_product(product_id, product_name, category, quantity, cost_price, selling_price):
     try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        sql = """UPDATE products 
        SET product_name = %s,
            category = %s,
            quantity = %s,
            cost_price = %s,
            selling_price = %s
          
          WHERE product_id = %s"""

        values = (product_name, category, quantity, cost_price, selling_price, product_id)

        mycursor.execute(sql, values)

        mydb.commit()

        print("Product Updated Successfully!")

     except Error as e:
         
         print(f"Error: {e}")

     finally:

          if mydb.is_connected():
                           
               mycursor.close()
              
               mydb.close()
             

def delete_product(product_id):
     try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        sql = "DELETE FROM products WHERE product_id = %s"

        mycursor.execute(sql, (product_id,))

        mydb.commit()

        print("Product Deleted Successfully!")

     except Error as e:
         
         print(f"Error: {e}")

     finally:
         if mydb.is_connected():
             
             mycursor.close()

             mydb.close()    


def get_product_by_id(product_id):
    try:
        mydb = connect_database()

        mycursor = mydb.cursor()

        sql = """ SELECT product_id, product_name, category, quantity, selling_price, cost_price
        FROM products
        WHERE product_id = %s
        """
        mycursor.execute(sql, (product_id,))

        product = mycursor.fetchone()

        mycursor.close()

        mydb.close()

        return product

    except Error as e:
        print(e)

        return None


     