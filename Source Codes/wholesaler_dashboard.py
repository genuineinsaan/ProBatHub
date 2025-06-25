import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

def open_wholesaler_dashboard(wholesaler_email):
    def place_order():
        bat_id = selected_bat.get()
        if not bat_id:
            messagebox.showerror("Error", "Please select a bat to order.")
            return
        try:
            qty = int(qty_entry.get())
            if qty <= 0:
                raise ValueError
            conn = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM bats WHERE bat_id = %s", (bat_id,))
            available = cursor.fetchone()[0]
            if qty > available:
                messagebox.showerror("Stock Error", f"Only {available} bats are available.")
                conn.close()
                return
            cursor.execute("INSERT INTO orders (wholesaler_email, bat_id, quantity, status) VALUES (%s, %s, %s, 'pending')",
                           (wholesaler_email, bat_id, qty))
            conn.commit()
            conn.close()
            messagebox.showinfo("Order Placed", "Order placed and pending confirmation.")
            load_bats()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid quantity.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_bats():
        for widget in bat_frame.winfo_children():
            widget.destroy()
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")
            cursor = conn.cursor()
            cursor.execute("SELECT bat_id, name, brand, category, price, quantity FROM bats WHERE active = TRUE")
            bats = cursor.fetchall()
            conn.close()
            if not bats:
                tk.Label(bat_frame, text="No bats available.", fg="gray").pack()
                return
            for bat_id, name, brand, category, price, qty in bats:
                text = f"{brand} - {name} ({category}) | ₹{price} | Stock: {qty}"
                tk.Radiobutton(bat_frame, text=text, variable=selected_bat, value=bat_id, anchor="w", justify="left").pack(fill="x", padx=10, pady=2)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_my_orders():
        top = tk.Toplevel(root)
        top.title("My Orders")
        top.geometry("600x400")
        frame = tk.Frame(top)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.name, b.brand, o.quantity, o.status
                FROM orders o
                JOIN bats b ON o.bat_id = b.bat_id
                WHERE o.wholesaler_email = %s
                ORDER BY o.order_date DESC
            """, (wholesaler_email,))
            orders = cursor.fetchall()
            conn.close()
            for name, brand, qty, status in orders:
                color = {"pending": "blue", "confirmed": "green"}.get(status, "red")
                tk.Label(frame, text=f"{brand} - {name} | Qty: {qty} | {status.capitalize()}", fg=color, anchor="w", justify="left").pack(fill="x", pady=2)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def logout():
        root.destroy()
        subprocess.Popen([sys.executable, "login_window.py"])

    root = tk.Tk()
    root.title("WHOLESALER WINDOW")
    w, h = root.winfo_screenwidth()//2, root.winfo_screenheight()//2
    x, y = (root.winfo_screenwidth()-w)//2, (root.winfo_screenheight()-h)//2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(False, False)

    tk.Label(root, text=f"WELCOME, {wholesaler_email}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(root, text="REFRESH", command=load_bats).pack(pady=5)

    selected_bat = tk.IntVar()
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    bat_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=bat_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=5)
    scrollbar.pack(side="right", fill="y")
    bat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    qty_frame = tk.Frame(root)
    qty_frame.pack(pady=10)
    tk.Label(qty_frame, text="QUANTITY:").pack(side="left")
    qty_entry = tk.Entry(qty_frame, width=5)
    qty_entry.insert(0, "1")
    qty_entry.pack(side="left", padx=5)

    tk.Button(root, text="PLACE ORDER", width=20, command=place_order).pack(pady=10)
    tk.Button(root, text="ORDER HISTORY", width=20, command=view_my_orders).pack(pady=5)
    tk.Button(root, text="LOGOUT", width=20, fg="red", command=logout).pack(pady=5)

    load_bats()
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        open_wholesaler_dashboard(sys.argv[1])
    else:
        print("Wholesaler email not provided.")
