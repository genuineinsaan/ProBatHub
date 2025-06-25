import tkinter as tk
from tkinter import messagebox
import mysql.connector

def db_connect():
    return mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="probathub")

def fetch_question():
    email, role = email_entry.get().strip(), role_var.get()
    if not email:
        return messagebox.showerror("Error", "Please enter your email.")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT question FROM users WHERE email = %s AND role = %s", (email, role))
        result = cursor.fetchone()
        conn.close()
        if result:
            question_var.set(result[0])
            answer_frame.pack(pady=5)
        else:
            messagebox.showerror("Not Found", "No user found with this email and role.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def verify_answer():
    email, role = email_entry.get().strip(), role_var.get()
    answer = answer_entry.get().strip()
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND role = %s AND answer = %s", (email, role, answer))
        if cursor.fetchone():
            reset_frame.pack(pady=5)
        else:
            messagebox.showerror("Error", "Incorrect answer.")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def reset_password():
    email, role = email_entry.get().strip(), role_var.get()
    new_pass, confirm_pass = new_pass_entry.get(), confirm_pass_entry.get()
    if new_pass != confirm_pass:
        return messagebox.showerror("Error", "Passwords do not match.")
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE email = %s AND role = %s", (new_pass, email, role))
        conn.commit(); conn.close()
        messagebox.showinfo("Success", "Password reset successful.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# -------------------- GUI --------------------
root = tk.Tk()
root.title("FORGOT PASSWORD")
w, h = root.winfo_screenwidth() // 2, int(root.winfo_screenheight() / 2.2)
x, y = (root.winfo_screenwidth() - w) // 2, (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(False, False)

tk.Label(root, text="FORGOT PASSWORD", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="SELECT ROLE:").pack()
role_var = tk.StringVar(value="manufacturer")
tk.OptionMenu(root, role_var, "manufacturer", "wholesaler").pack()

tk.Label(root, text="EMAIL:").pack()
email_entry = tk.Entry(root, width=30); email_entry.pack(pady=5)

tk.Button(root, text="SHOW SECURITY QUESTIONS", command=fetch_question).pack(pady=5)

question_var = tk.StringVar()
tk.Label(root, textvariable=question_var, font=("Arial", 10, "italic")).pack()

# Security Answer Section
answer_frame = tk.Frame(root)
tk.Label(answer_frame, text="SECURITY ANSWER:").pack()
answer_entry = tk.Entry(answer_frame, width=30); answer_entry.pack()
tk.Button(answer_frame, text="VERIFY ANSWER", command=verify_answer).pack(pady=5)

# Password Reset Section
reset_frame = tk.Frame(root)
tk.Label(reset_frame, text="NEW PASSWORD:").pack()
new_pass_entry = tk.Entry(reset_frame, width=30, show="*"); new_pass_entry.pack()
tk.Label(reset_frame, text="CONFIRM PASSWORD:").pack()
confirm_pass_entry = tk.Entry(reset_frame, width=30, show="*"); confirm_pass_entry.pack()
tk.Button(reset_frame, text="RESET PASSWORD", command=reset_password).pack(pady=5)

root.mainloop()
