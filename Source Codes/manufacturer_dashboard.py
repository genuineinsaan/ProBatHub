import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

def open_manufacturer_dashboard():
    def db_connect():
        return mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")

    def load_pending_orders():
        for w in orders_frame.winfo_children():
            w.destroy()
        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_id, o.wholesaler_email, b.name, b.brand, b.category, o.quantity
                FROM orders o JOIN bats b ON o.bat_id = b.bat_id
                WHERE o.status = 'pending' ORDER BY o.order_date DESC
            """)
            orders = cursor.fetchall()
            conn.close()
            if not orders:
                tk.Label(orders_frame, text="NO PENDING REQUESTS.", fg="gray").pack()
                return
            for oid, email, name, brand, cat, qty in orders:
                text = f"Wholesaler: {email}\nBat: {brand} - {name} ({cat})\nQty: {qty}"
                box = tk.Frame(orders_frame, bd=1, relief="solid", padx=10, pady=5)
                tk.Label(box, text=text, justify="left", anchor="w").pack(anchor="w")
                f = tk.Frame(box); f.pack(pady=5)
                tk.Button(f, text="CONFIRM ORDER", command=lambda oid=oid: update_status(oid, "confirmed")).pack(side="left", padx=5)
                tk.Button(f, text="CANCEL ORDER", command=lambda oid=oid: update_status(oid, "denied")).pack(side="left", padx=5)
                box.pack(pady=10, fill="x")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_status(oid, status):
        try:
            conn = db_connect()
            cursor = conn.cursor()
            if status == "confirmed":
                cursor.execute("SELECT bat_id, quantity FROM orders WHERE order_id = %s", (oid,))
                bat_id, qty = cursor.fetchone()
                cursor.execute("SELECT quantity FROM bats WHERE bat_id = %s", (bat_id,))
                stock = cursor.fetchone()[0]
                if qty > stock:
                    messagebox.showerror("Stock Error", "Not enough bats in stock.")
                    conn.close(); return
                cursor.execute("UPDATE bats SET quantity = quantity - %s WHERE bat_id = %s", (qty, bat_id))
            cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, oid))
            conn.commit(); conn.close()
            messagebox.showinfo("Status Updated", f"Order marked as '{status}'.")
            load_pending_orders()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def open_script(script): subprocess.Popen([sys.executable, script])

    def view_all_orders():
        top = tk.Toplevel(root)
        top.title("ALL REQUESTS")
        top.geometry("600x400")
        f = tk.Frame(top); f.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_id, o.wholesaler_email, b.name, b.brand, o.quantity, o.status
                FROM orders o JOIN bats b ON o.bat_id = b.bat_id
                ORDER BY o.order_date DESC
            """)
            for oid, email, name, brand, qty, status in cursor.fetchall():
                color = {"pending": "blue", "confirmed": "green"}.get(status, "red")
                tk.Label(f, text=f"{email} ordered {brand}-{name} (Qty: {qty}) → {status.capitalize()}",
                         fg=color, anchor="w", justify="left").pack(fill="x", pady=2)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("MANUFACTURE WINDOW")
    w, h = root.winfo_screenwidth()//2, root.winfo_screenheight()//2
    x, y = (root.winfo_screenwidth()-w)//2, (root.winfo_screenheight()-h)//2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(False, False)

    tk.Label(root, text="PENDING REQUESTS", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(root, text="REFRESH REQUESTS", width=20, command=load_pending_orders).pack(pady=5)
    tk.Button(root, text="ADD PRODUCT STOCK", width=20, command=lambda: open_script("add_product_stock.py")).pack(pady=5)
    tk.Button(root, text="VIEW PRODUCT STOCK", width=20, command=lambda: open_script("product_stock.py")).pack(pady=5)
    tk.Button(root, text="ADD PRODUCT ID ", width=20, command=lambda: open_script("add_product_id.py")).pack(pady=5)
    tk.Button(root, text="ORDER HISTORY", width=20, command=view_all_orders).pack(pady=5)
    tk.Button(root, text="LOGOUT", width=20, fg="red", command=lambda: [root.destroy(), open_script("login_window.py")]).pack(pady=10)

    orders_frame = tk.Frame(root)
    orders_frame.pack(expand=True, fill="both", padx=20)

    load_pending_orders()
    root.mainloop()

if __name__ == "__main__":
    open_manufacturer_dashboard()
