from product_db import (
    add_product,
    view_product,
    update_product,
    delete_product,
    get_product_by_id
)

from sales_db import (
    record_sale,
    view_sales
)

from reports import (
    low_stock_report,
    daily_sales_report
)


class Product:
    def __init__(self, product_name, category, quantity, cost_price, selling_price, created_at, product_id=None):
        self.product_name = product_name
        self.category = category
        self.quantity = quantity
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.created_at = created_at
        self.product_id = product_id

    def display_info(self):
        print(f"\nProduct ID: {self.product_id}")
        print(f"Product Name: {self.product_name}")
        print(f"Category: {self.category}")
        print(f"Quantiy: {self.quantity}")
        print(f"Cost Price: {self.cost_price}")
        print(f"Selling Price: {self.selling_price}")
        print(f"Created At: {self.created_at}")


class Sale:
    def __init__(self, product_id, quantity_sold, unit_price, total_amount, sale_date, sale_id=None):
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.sale_date = sale_date
        self.sale_id = sale_id

    def display_info(self):
        print(f"\nSale ID: {self.sale_id}")
        print(f"Product ID: {self.product_id}")
        print(f"Quantity Sold: {self.quantity_sold}")
        print(f"Unit Price: {self.unit_price}")
        print(f"Total Amount: {self.total_amount}")
        print(f"Sale Date: {self.sale_date}")

        

class Inventory:
    def __init__(self):
        pass

    def operations(self):
        while True:

           print("=" * 40)
           print("\t📦 INVENTORY & SALES SYSTEM")
           print("=" * 40)
           print("1. 📦 Add Product")
           print("2. 👀 View Products")
           print("3. 🖊 Update Product")
           print("4. 🗑 Delete Product")
           print("5. 📝 Record Sale")
           print("6. 🧾 View Sales")
           print("7. 📊 Daily Sales Report")
           print("8. ⚠ Low Stock Report")
           print("9. 🚪 Exit\n")
           print("=" * 40)
           

           choice = input("Enter your choice (1-9): ")

           if choice == "1":
            try:
                product_name = input("Enter Product Name: ")
                category = input("Enter Category: ")
                quantity = int(input("Enter Quantity: "))
                cost_price = eval(input("Enter Cost Price: "))
                selling_price = eval(input("Enter Sell Price: "))

                add_product(product_name, category, quantity, cost_price, selling_price)

            except ValueError:
                print("❌ Error: Invalid input. Please enter the correct data types.")   

           elif choice == "2":
               record = view_product()

               if record:
                   for record in record:
                       print(record)

               else:
                   print("No record found!")   

           elif choice == "3":
               try:
                   product_id = int(input("Enter Product ID to Update: "))
                   product_name = input("Enter Product Name: ")
                   category = input("Enter Category: ")
                   quantity = int(input("Enter Quantity: "))
                   cost_price = eval(input("Enter Cost Price: "))
                   selling_price = eval(input("Enter Sell Price: "))

                   update_product(product_id, product_name, category, quantity, cost_price, selling_price)

               except ValueError:
                   print("❌ Error: Invalid input. Please enter correct numerical values!")

           elif choice == "4":
               try:
                   product_id = int(input("Enter Product ID: "))
                   delete_product(product_id)

               except ValueError:
                   print("❌ Please enter a valid integer for Product ID")

           elif choice == "5":
               try:
                   product_id = int(input("Enter Product ID: "))
                   quantity = int(input("Enter Quantity: "))
                   product = get_product_by_id(product_id)

                   if not product:
                       print("❌ Product not found.")
                       return

                   available_quantity = product[2]
                   unit_price = product[3]

                   if quantity <= 0:
                       print("❌ Quantity must be greater than zero.")
                       return

                   if quantity > available_quantity:
                       print("❌ Not enough stock available.")
                       return

                   total_amount = quantity * unit_price

                   record_sale(product_id, quantity, unit_price, total_amount)

                   print("✅ Sale recorded successfully.")
                   print(f"Unit Price: ₦{unit_price}")
                   print(f"Total Amount: ₦{total_amount}")

               except ValueError:
                   print("❌ Error: Invalid input. Please enter the correct data.")

           elif choice == "6":
               records = view_sales()

               if records:
                   for record in records:
                       print(record)

               else:
                   print("No records found!")   
           elif choice == "7":
               totals, breakdown = daily_sales_report()   
               if totals:    
                   print("=" * 40)
                   print("           DAILY SALES REPORT")
                   print("=" * 40)
                   print(f"Total Items Sold: {totals[0]}")
                   print(f"Total Revenue: ₦{totals[1]:,.0f}")
                   print(f"Total Profit: ₦{totals[2]:,.0f}")
                   print("=" * 40)

           elif choice == "8":
               results = low_stock_report(10)

               for row in results:
                   print(f"{row[0]} - only {row[1]} left")        

           elif choice == '9':
               print("Exiting....")
               break

           else:
               print("❌ Invalid choice. Please try again!")
               continue                                 

                      
                                 


if __name__ == "__main__":

    system = Inventory()

    system.operations()
