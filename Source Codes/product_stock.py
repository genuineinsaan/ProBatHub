import tkinter as tk
from tkinter import messagebox
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="sanjana1432", database="probathub"
    )

def open_bat_manager():
    def load_bats():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT bat_id, name, brand, category, price, quantity FROM bats WHERE active = TRUE")
            bats = cursor.fetchall(); conn.close()

            if not bats:
                tk.Label(scrollable_frame, text="No bats found.", fg="gray").pack()
                return

            for bat_id, name, brand, category, price, qty in bats:
                box = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=5)
                tk.Label(box, text=f"{brand} - {name} ({category})", font=("Arial", 10, "bold")).pack(anchor="w")
                tk.Label(box, text=f"Price: ₹{price}   |   Quantity: {qty}").pack(anchor="w")

                entry_frame = tk.Frame(box); entry_frame.pack(pady=3)
                price_entry = tk.Entry(entry_frame, width=8); price_entry.insert(0, str(price))
                qty_entry = tk.Entry(entry_frame, width=5); qty_entry.insert(0, str(qty))

                for i, (label, entry) in enumerate([("Price:", price_entry), ("Qty:", qty_entry)]):
                    tk.Label(entry_frame, text=label).grid(row=0, column=i * 2)
                    entry.grid(row=0, column=i * 2 + 1, padx=5)

                tk.Button(
                    box,
                    text="Update",
                    command=lambda i=bat_id, p=price_entry, q=qty_entry: update_bat(i, p.get(), q.get())
                ).pack(pady=5)

                box.pack(pady=8, fill="x")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_bat(bat_id, new_price, new_qty):
        try:
            new_price = float(new_price)
            new_qty = int(new_qty)
        except ValueError:
            return messagebox.showerror("Invalid Input", "Price must be a number and quantity an integer.")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE bats SET price=%s, quantity=%s WHERE bat_id=%s", (new_price, new_qty, bat_id))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", "Bat updated.")
            load_bats()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # --- GUI Setup ---
    root = tk.Tk()
    root.title("VIEW PRODUCT STOCK")
    w, h = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2
    root.geometry(f"{w}x{h}+{w//2}+{h//2}")
    root.resizable(False, False)

    tk.Label(root, text="PRODUCT INVENTORY", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(root, text="REFRESH INVENTORY", command=load_bats).pack()

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
    scrollbar.pack(side="right", fill="y")

    load_bats()
    root.mainloop()

if __name__ == "__main__":
    open_bat_manager()
