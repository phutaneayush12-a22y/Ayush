import tkinter as tk
from tkinter import messagebox

def login_screen():
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("300x200")

    tk.Label(login_win, text="User ID:").pack(pady=5)
    user_entry = tk.Entry(login_win)
    user_entry.pack()

    tk.Label(login_win, text="Password:").pack(pady=5)
    pass_entry = tk.Entry(login_win, show="*")
    pass_entry.pack()

    def validate_login():
        user_id = user_entry.get().strip()
        password = pass_entry.get().strip()

        if "@" not in user_id or not user_id.endswith(".com"):
            messagebox.showerror("Error", "Invalid User ID. Must contain '@' and end with '.com'.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

        messagebox.showinfo("Success", "Login Successful!")
        login_win.destroy()
        profile = load_profile()
        main_ui(profile)

    tk.Button(login_win, text="Login", command=validate_login).pack(pady=20)

    login_win.mainloop()
    
if __name__ == "_main_":
    login_screen()