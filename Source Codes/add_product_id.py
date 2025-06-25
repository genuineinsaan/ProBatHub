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

def open_add_product_id_window():
    def generate_and_add_id():
        brand = brand_var.get().strip().upper()
        category = category_var.get().strip().upper()

        if not brand or not category:
            return messagebox.showerror("Missing Data", "Please enter both brand and category.")

        product_id = brand[:3] + "-" + category[:3]
        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO product_ids (product_id, brand, category) VALUES (%s, %s, %s)",
                (product_id, brand, category)
            )
            conn.commit(); conn.close()
            messagebox.showinfo("Success", f"Product ID '{product_id}' added.")
            brand_var.set(""); category_var.set("")
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Duplicate", f"Product ID '{product_id}' already exists.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    root = tk.Tk()
    root.title("ADD PRODUCT ID")

    w, h = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 3
    root.geometry(f"{w}x{h}+{w//2}+{h//2}")
    root.resizable(False, False)

    tk.Label(root, text="ADD PRODUCT ID", font=("Arial", 16, "bold")).pack(pady=10)

    frame = tk.Frame(root); frame.pack(pady=10)

    brand_var, category_var = tk.StringVar(), tk.StringVar()

    tk.Label(frame, text="CRICKET BRAND NAME:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame, textvariable=brand_var, width=30).grid(row=0, column=1)

    tk.Label(frame, text="CATEGORY:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame, textvariable=category_var, width=30).grid(row=1, column=1)

    tk.Button(root, text="GENERATE PRODUCT ID", command=generate_and_add_id).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_add_product_id_window()
