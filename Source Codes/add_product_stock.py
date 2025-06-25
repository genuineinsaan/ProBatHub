import tkinter as tk
from tkinter import messagebox
import mysql.connector

def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sanjana1432",
        database="probathub"
    )

def open_add_bat_window():
    def fetch_product_ids():
        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT product_id FROM product_ids")
            ids = [row[0] for row in cursor.fetchall()]
            conn.close()
            return ids or ["-- No Product IDs --"]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return ["-- No Product IDs --"]

    def refresh_dropdown():
        ids = fetch_product_ids()
        product_id_var.set(ids[0])
        menu = product_id_menu["menu"]
        menu.delete(0, "end")
        for pid in ids:
            menu.add_command(label=pid, command=lambda v=pid: product_id_var.set(v))

    def add_bat():
        pid, name, price, qty = product_id_var.get(), name_var.get().strip(), price_var.get(), quantity_var.get()
        if pid == "-- No Product IDs --":
            return messagebox.showerror("Invalid Product ID", "Please add Product IDs first.")
        if not all([pid, name, price, qty]):
            return messagebox.showerror("Missing Data", "Please fill all fields.")
        try:
            price, qty = float(price), int(qty)
        except ValueError:
            return messagebox.showerror("Invalid Input", "Price must be a number and quantity an integer.")

        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT brand, category FROM product_ids WHERE product_id = %s", (pid,))
            result = cursor.fetchone()
            if not result:
                return messagebox.showerror("Data Error", "Product ID not found.")

            brand, category = result
            cursor.execute("""
                INSERT INTO bats (product_id, name, price, quantity, brand, category)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (pid, name, price, qty, brand, category))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", "Bat added to inventory.")
            name_var.set(""); price_var.set(""); quantity_var.set("")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # === GUI ===
    root = tk.Tk()
    root.title("ADD PRODUCT STOCK")
    w, h = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2
    root.geometry(f"{w}x{h}+{w//2}+{h//2}"); root.resizable(False, False)

    tk.Label(root, text="ADD PRODUCT STOCK", font=("Arial", 16, "bold")).pack(pady=10)

    frame = tk.Frame(root); frame.pack(pady=10)

    # Dropdown
    tk.Label(frame, text="PRODUCT ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    product_ids = fetch_product_ids()
    product_id_var = tk.StringVar(value=product_ids[0])
    product_id_menu = tk.OptionMenu(frame, product_id_var, *product_ids)
    product_id_menu.grid(row=0, column=1)
    tk.Button(frame, text="REFRESH ID", command=refresh_dropdown).grid(row=0, column=2, padx=10)

    # Name
    name_var = tk.StringVar()
    tk.Label(frame, text="PRODUCT NAME:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(frame, textvariable=name_var, width=30).grid(row=1, column=1)

    # Price
    price_var = tk.StringVar()
    tk.Label(frame, text="PRICE IN(₹):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(frame, textvariable=price_var, width=30).grid(row=2, column=1)

    # Quantity
    quantity_var = tk.StringVar()
    tk.Label(frame, text="QUANTITY:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(frame, textvariable=quantity_var, width=30).grid(row=3, column=1)

    # Add Button
    tk.Button(root, text="ADD PRODUCT", command=add_bat, width=20).pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    open_add_bat_window()
