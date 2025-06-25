import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

def toggle_password():
    password_entry.config(show='' if show_password_var.get() else '*')

def on_role_change(*_):
    if role_var.get() == "wholesaler":
        gst_label.pack(after=show_pass_check, pady=5)
        gst_entry.pack(after=gst_label)
    else:
        gst_label.pack_forget()
        gst_entry.pack_forget()

def login():
    email = email_entry.get().strip()
    pwd = password_entry.get().strip()
    role = role_var.get()
    gst = gst_entry.get().strip() if role == "wholesaler" else None
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")
        cursor = conn.cursor()
        q = "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s"
        q += " AND gst_number=%s" if role == "wholesaler" else ""
        vals = (email, pwd, role, gst) if role == "wholesaler" else (email, pwd, role)
        cursor.execute(q, vals)
        if cursor.fetchone():
            messagebox.showinfo("Login Success", f"Welcome, {role.capitalize()}!")
            root.destroy()
            script = "manufacturer_dashboard.py" if role == "manufacturer" else "wholesaler_dashboard.py"
            subprocess.Popen([sys.executable, script] + ([email] if role == "wholesaler" else []))
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def open_script(script): subprocess.Popen([sys.executable, script])

root = tk.Tk()
root.title("PROBATHUB LOGIN WINDOW")
w, h = root.winfo_screenwidth()//2, int(root.winfo_screenheight()/1.7)
root.geometry(f"{w}x{h}+{w//2}+{h//2}")
root.resizable(False, False)

main = tk.Frame(root); main.pack(expand=True)
tk.Label(main, text="LOGIN PAGE", font=("Arial", 20, "bold")).pack(pady=20)

tk.Label(main, text="ROLE:").pack()
role_var = tk.StringVar(value="manufacturer")
tk.OptionMenu(main, role_var, "manufacturer", "wholesaler").pack()
role_var.trace("w", on_role_change)

tk.Label(main, text="EMAIL:").pack(pady=5)
email_entry = tk.Entry(main, width=30); email_entry.pack()

tk.Label(main, text="PASSWORD:").pack(pady=5)
password_entry = tk.Entry(main, show="*", width=30); password_entry.pack()

show_password_var = tk.BooleanVar()
show_pass_check = tk.Checkbutton(main, text="SHOW PASSWORD", variable=show_password_var, command=toggle_password)
show_pass_check.pack(pady=5)

gst_label = tk.Label(main, text="GST NUMBER:")
gst_entry = tk.Entry(main, width=30)

tk.Button(main, text="LOGIN", command=login, width=20).pack(pady=10)
tk.Button(main, text="REGISTER -AS WHOLESALER", command=lambda: open_script("register.py"), width=20).pack(pady=5)
tk.Button(main, text="FORGOT PASSWORD !", command=lambda: open_script("forgot_password.py")).pack()

on_role_change()
root.mainloop()
