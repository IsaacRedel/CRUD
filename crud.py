import sqlite3
import tkinter as tk
from tkinter import messagebox
import re

# Connect to database or create a new one if it doesn't exist
conn = sqlite3.connect("database.db")

# Create a table
conn.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, 
                                                   name TEXT, 
                                                   email TEXT UNIQUE)""")
conn.commit()

# Tkinter UI
root = tk.Tk()
root.title("CRUD Interface")
root.resizable(width=tk.FALSE, height=tk.FALSE)

# Function to validate email address
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Functions to handle CRUD operations
def create_user():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    if not name or not email:
        messagebox.showerror("Error", "Name and email cannot be empty")
        return
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return
    try:
        conn.execute("INSERT INTO users (name, email) VALUES (?,?)", (name, email))
        conn.commit()
        messagebox.showinfo("Success", "User created successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists")

def read_user():
    cursor = conn.execute("SELECT * FROM users")
    user_info = ""
    for row in cursor:
        user_info += f"ID: {row[0]}\nName: {row[1]}\nEmail: {row[2]}\n\n"
    messagebox.showinfo("User information", user_info)

def update_user():
    id = id_entry.get().strip()
    name = name_entry.get().strip()
    if not id or not name:
        messagebox.showerror("Error", "ID and name cannot be empty")
        return
    try:
        conn.execute("UPDATE users SET name=? WHERE id=?", (name, id))
        conn.commit()
        messagebox.showinfo("Success", "User updated successfully")
    except sqlite3.Error:
        messagebox.showerror("Error", "User with the specified ID does not exist")

def delete_user():
    id = id_entry.get().strip()
    if not id:
        messagebox.showerror("Error", "ID cannot be empty")
        return
    try:
        conn.execute("DELETE FROM users WHERE id=?", (id,))
        conn.commit()
        messagebox.showinfo("Success", "User deleted successfully")
    except sqlite3.Error:
        messagebox.showerror("Error", "User with the specified ID does not exist")

# Labels
id_label = tk.Label(root, text="ID")
id_label.grid(row=0, column=0)
name_label = tk.Label(root, text="Name")
name_label.grid(row=1, column=0)
email_label = tk.Label(root, text="Email")
email_label.grid(row=2, column=0)

# Entries
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

# Buttons
create_button = tk.Button(root, text="Create", command=create_user)
create_button.grid(row=3, column=0)
read_button = tk.Button(root, text="Read", command=read_user)
read_button.grid(row=3, column=1)
update_button = tk.Button(root, text="Update", command=update_user)
update_button.grid(row=3, column=2)
delete_button = tk.Button(root, text="Delete", command=delete_user)
delete_button.grid(row=3, column=3)

root.mainloop()
