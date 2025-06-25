import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

def db_connect():
    return mysql.connector.connect(
        host="localhost", user="root", password="sanjana1432", database="probathub"
    )

def create_field(label, key, show=None):
    tk.Label(form_frame, text=label).pack(pady=3)
    entry = tk.Entry(form_frame, width=30, show=show)
    entry.pack()
    entries[key] = entry

def register():
    for key in ["email", "password", "confirm", "gst", "answer"]:
        if not entries.get(key) or not entries[key].get():
            messagebox.showerror("Error", f"{key.capitalize()} is required.")
            return
    if entries["password"].get() != entries["confirm"].get():
        messagebox.showerror("Error", "Passwords do not match.")
        return
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (role, company_name, product, shop_name, address, email, phone, gst_number, password, question, answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            "wholesaler", None, None,
            entries["shop_name"].get(),
            entries["address"].get(),
            entries["email"].get(),
            entries["phone"].get(),
            entries["gst"].get(),
            entries["password"].get(),
            entries["question"].get(),
            entries["answer"].get()
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
        go_to_login()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def go_to_login():
    root.destroy()
    subprocess.Popen([sys.executable, "login_window.py"])

root = tk.Tk()
root.title("ProBatHub Registration")
w, h = root.winfo_screenwidth()//2, int(root.winfo_screenheight()/1.4)
x, y = (root.winfo_screenwidth()-w)//2, (root.winfo_screenheight()-h)//2
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(False, False)

tk.Label(root, text="REGISTER", font=("Arial", 18, "bold")).pack(pady=10)
form_frame = tk.Frame(root)
form_frame.pack(pady=10)
entries = {}

create_field("Shop Name", "shop_name")
create_field("Address", "address")
create_field("Email", "email")
create_field("Phone Number", "phone")
create_field("GST Number", "gst")
create_field("Password", "password", show="*")
create_field("Confirm Password", "confirm", show="*")

questions = ["Your favorite sport?", "Your first school name?", "Your pet's name?", "Your best friend’s name?"]
q_var = tk.StringVar(value=questions[0])
tk.Label(form_frame, text="Security Question:").pack(pady=3)
tk.OptionMenu(form_frame, q_var, *questions).pack()
entries["question"] = q_var

create_field("Security Answer", "answer")

tk.Button(root, text="Register", command=register, width=20).pack(pady=5)
tk.Button(root, text="Back", command=go_to_login, width=20).pack(pady=5)

root.mainloop()
