import tkinter as tk
from tkinter.messagebox import *
from tkinter import ttk
from tkinter import simpledialog
from product_db import (
    add_product,
    get_product_by_id,
    update_product,
    view_product,
    delete_product
)
from sales_db import(
    record_sale,
    view_sales
)
from reports import(
    daily_sales_report,
    low_stock_report
)




root = tk.Tk()
root.title('📦 Inventory & Sales System')
root.geometry('400x500')



def open_view_products():
    top = tk.Toplevel(root)
    top.title("Products")

    columns = ("ID", "Name", "Category", "Quantity", "Cost Price", "Selling Price")
    tree = ttk.Treeview(top, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)    

    records = view_product()
    for row in records:
        tree.insert("", "end", values=row)

def open_add_products():
    top = tk.Toplevel(root)
    top.title("Add Products")
    top.geometry("400x300")

    tk.Label(top, text="Product Name").grid(row=0, column=0)
    name_entry= tk.Entry(top, font=('Verdana', 16), width=25)
    name_entry.grid(row=0, column=1)

    tk.Label(top, text="Category").grid(row=1, column=0)
    category_entry= tk.Entry(top, font=('Verdana', 16), width=25)
    category_entry.grid(row=1, column=1)


    tk.Label(top, text="Quantity").grid(row=2, column=0)
    quantity_entry= tk.Entry(top, font=('Verdana', 16), width=25)
    quantity_entry.grid(row=2, column=1)

    tk.Label(top, text="Cost Price").grid(row=3, column=0)
    cost_price_entry= tk.Entry(top, font=('Verdana', 16), width=25)
    cost_price_entry.grid(row=3, column=1)


    tk.Label(top, text="Selling Price").grid(row=4, column=0)
    selling_price_entry= tk.Entry(top, font=('Verdana', 16), width=25)
    selling_price_entry.grid(row=4, column=1)


    def submit_add_product():
        product_name = name_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())
        cost_price = float(cost_price_entry.get())
        selling_price = float(selling_price_entry.get())

        add_product(product_name, category, quantity, cost_price, selling_price)

        showinfo("Suucess", "Product added successfully!")
        top.destroy()



    tk.Button(top, text="Submit", command=submit_add_product).grid(row=5, column=0, columnspan=2)    
   

def open_update_product():
    product_id = simpledialog.askinteger("Update Product", "Enter Product ID:")
    if not product_id:
        return # User cancel or enter nothing.

    product = get_product_by_id(product_id)
    if not product:
        showerror("Error", "Product not found.")
        return


    top = tk.Toplevel(root)
    top.title("Update Product")
    top.geometry("400x300")

    tk.Label(top, text="Product Name").grid(row=0, column=0)
    name_entry = tk.Entry(top, font=('Verdana', 16), width=25)
    name_entry.insert(0, product[1])
    name_entry.grid(row=0, column=1)


    tk.Label(top, text="Category").grid(row=1, column=0)
    category_entry = tk.Entry(top, font=('Verdana', 16), width=25)
    category_entry.insert(0, product[2])
    category_entry.grid(row=1, column=1)

    tk.Label(top, text="Quantity").grid(row=2, column=0)
    quantity_entry = tk.Entry(top, font=('Verdana', 16), width=25)
    quantity_entry.insert(0, product[3])
    quantity_entry.grid(row=2, column=1)

    tk.Label(top, text="Cost Price").grid(row=3, column=0)
    cost_price_entry = tk.Entry(top, font=('Verdana', 16), width=25)
    cost_price_entry.insert(0, product[4])
    cost_price_entry.grid(row=3, column=1)    

    tk.Label(top, text="Selling Price").grid(row=4, column=0)
    selling_price_entry = tk.Entry(top, font=('Verdana', 16), width=25)
    selling_price_entry.insert(0, product[5])
    selling_price_entry.grid(row=4, column=1)

    def submit_update_product():
        new_name = name_entry.get()
        new_category = category_entry.get()
        new_quantity = int(quantity_entry.get())
        new_cost_price = float(cost_price_entry.get())
        new_selling_price = float(selling_price_entry.get())

        update_product(product_id, new_name, new_category, new_quantity, new_cost_price, new_selling_price)

        showinfo("Success", "Product updated successfully!")
        top.destroy()

    tk.Button(top, text="Submit", command=submit_update_product).grid(row=5, column=0, columnspan=2)    



def open_delete_product():
    product_id = simpledialog.askinteger("Delete Product", "Enter Product ID:")
    if not product_id:
        return

    product = get_product_by_id(product_id)
    if not product:
        showerror("Error", "Product not found.")
        return

    confirm = askyesno("Confirm Delete", f"Delete '{product[1]}'? This cannot be undone.")
    if confirm:
        delete_product(product_id)
        showinfo("Success", "Product deleted successfully!")

    tk.Button(text="Submit", command=open_update_product).grid(row=5, column=0, columnspan=2)    


def open_record_sale():
    product_id = simpledialog.askinteger("Record Sale", "Enter Product ID:")
    if not product_id:
        return

    product = get_product_by_id(product_id)
    if not product:
        showerror("Error", "Product not found.")
        return

    available_quantity = product[3]
    unit_price = product[4]

    top = tk.Toplevel(root)
    top.title("Record Sale")
    top.geometry("300x150")

    tk.Label(top, text=f"Product: {product[1]}").grid(row=0, column=0, columnspan=2)
    tk.Label(top, text="Quantity").grid(row=1, column=0)
    quantity_entry = tk.Entry(top, font=('Verdana, 14'), width=15)
    quantity_entry.grid(row=1, column=1)

    def submit_sale():

        quantity = int(quantity_entry.get())

        if quantity <= 0:
            showerror("Error", "Quantity must be greater than zero.")
            return
        if quantity > available_quantity:
            showerror("Error", "Not enough stock available.")
            return

        total_amount = quantity * unit_price
        

        record_sale(product_id, quantity, unit_price, total_amount)
        showinfo("Success", "Sale recorded successfully!")
        top.destroy()

    tk.Button(top, text="Submit", command=submit_sale).grid(row=2, column=0, columnspan=2)    


def open_view_sales():
    top = tk.Toplevel(root)
    top.title("Sales")

    columns = ("Sale ID", "Product ID", "Quantity Sold", "Unit Price", "Total Amount")
    tree = ttk.Treeview(top, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)    

    records = view_sales()
    for row in records:
        tree.insert("", "end", values=row)

    

def open_daily_sales_report():
    totals, breakdown = daily_sales_report()

    top = tk.Toplevel(root)
    top.title("Daily Sales Report")
    top.geometry("450x400")

    if totals:
        tk.Label(top, text=f"Total Items Sold: {totals[0]}", font=("Verdana",12)).pack(pady=5)
        tk.Label(top, text=f"Total Revenue: ₦{totals[1]:,.0f}", font=("Verdana",12)).pack(pady=5)
        tk.Label(top, text=f"Total Profit: ₦{totals[2]:,.0f}", font=("Verdana",12)).pack(pady=5)

        columns = ("Product", "Quantity Sold", "Revenue", "Profit")
        tree = ttk.Treeview(top, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        tree.pack(fill="both", expand=True, pady=10)
        
        for row in breakdown:
            tree.insert("", "end", values=row)    

    else:
        tk.Label(top, text="No sales recorded today.", font=("Verdana", 12)).pack(pady=20)

        


def open_low_stock_report():
    theshold = simpledialog.askinteger("Low Stock Report", "Show products below what quantity?")
    if not theshold:
        return

    records = low_stock_report(theshold)

    top = tk.Toplevel(root)
    top.title("Low Stock Report")
    top.geometry("350x300")

    if not records:
        tk.Label(top, text="No low stock products.", font=("Verdana", 12)).pack(pady=2)
        return

    columns = ("Product", "Quantity")
    tree = ttk.Treeview(top, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    for row in records:
        tree.insert("", "end", values=row)    


def confirm_exit():
    if askyesno("Exit", "Are you sure you want to exit?"):        
        root.destroy()


                






label = tk.Label()
label.configure(text='📦 Inventory & Sales System')
label.pack(pady=10)

tk.Button(root, text='👀 View Products', font=('Verdana, 12'), width=25, command=open_view_products).pack(pady=5, padx=5)
tk.Button(root, text='📦 Add Product', font=('Verdana, 12'), width=25, command=open_add_products).pack(pady=5, padx=5)
tk.Button(root, text='🖊 Update Product', font=('Verdana, 12'), width=25, command=open_update_product).pack(pady=5, padx=5)
tk.Button(root, text='🗑 Delete Product', font=('Verdana, 12'), width=25, command=open_delete_product).pack(pady=5, padx=5)
tk.Button(root, text='📝 Record Sale', font=('Verdana, 12'), width=25, command=open_record_sale).pack(pady=5, padx=5)
tk.Button(root, text='🧾 View Sales', font=('Verdana, 12'), width=25, command=open_view_sales).pack(pady=5, padx=5)
tk.Button(root, text='📊 Daily Sales Report', font=('Verdana, 12'), width=25, command=open_daily_sales_report).pack(pady=5, padx=5)
tk.Button(root, text='⚠ Low Stock Report', font=('Verdana, 12'), width=25, command=open_low_stock_report).pack(pady=5, padx=5)
tk.Button(root, text='🚪 Exit', font=('Verdana, 12'), width=25, command=confirm_exit).pack(pady=5, padx=5)







root.mainloop()

