import os
import base64
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

# --- 1. DATABASE LOGIC ---

def setup_database():
    # Creates a local .db file and builds the table based on your ER Diagram
    conn = sqlite3.connect("file_history.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FileOperation (
            Operation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Timestamp TEXT,
            Operation_Type TEXT,
            File_Path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_operation(operation_type, file_path):
    # Inserts a new record into the database every time a file is processed
    conn = sqlite3.connect("file_history.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO FileOperation (Timestamp, Operation_Type, File_Path) VALUES (?, ?, ?)",
                   (timestamp, operation_type, file_path))
    conn.commit()
    conn.close()

# --- 2. CORE CRYPTOGRAPHY LOGIC ---

def get_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filename, password):
    salt = os.urandom(16)
    key = get_key_from_password(password, salt)
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    encrypted_filename = filename + ".encrypted"
    with open(encrypted_filename, "wb") as file:
        file.write(salt + encrypted_data)
        
    os.remove(filename)

def decrypt_file(filename, password):
    with open(filename, "rb") as file:
        file_data = file.read()

    salt = file_data[:16]
    encrypted_data = file_data[16:]

    key = get_key_from_password(password, salt)
    f = Fernet(key)

    try:
        decrypted_data = f.decrypt(encrypted_data)
        
        if filename.endswith(".encrypted"):
            decrypted_filename = filename[:-10]
        else:
            decrypted_filename = filename + ".decrypted"
            
        with open(decrypted_filename, "wb") as file:
            file.write(decrypted_data)
            
        os.remove(filename)
        return True 
        
    except InvalidToken:
        return False 

# --- 3. GUI LOGIC ---

def start_gui():
    # Initialize the database when the app starts
    setup_database()

    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  

    window = ctk.CTk()
    window.title("Secure File Encryption Tool")
    window.geometry("500x550") # Made the window slightly taller for the new button
    
    title_label = ctk.CTkLabel(window, text="Secure File Encryption Tool", font=("Arial", 20, "bold"))
    title_label.pack(pady=30)
    
    selected_file_path = ""
    
    def browse_file():
        nonlocal selected_file_path
        filepath = filedialog.askopenfilename()
        if filepath:
            selected_file_path = filepath
            file_status_label.configure(text=f"Selected:\n{selected_file_path}", text_color="#569cd6")

    def gui_encrypt():
        if selected_file_path:
            password = simpledialog.askstring("Password", "Create a password for this file:", show='*')
            if password: 
                encrypt_file(selected_file_path, password)
                # Log the successful operation to the database!
                log_operation("Encrypt", selected_file_path)
                
                messagebox.showinfo("Success", "File securely encrypted with your password!")
                file_status_label.configure(text="No file selected", text_color="gray")
        else:
            messagebox.showerror("Error", "Please select a file first!")

    def gui_decrypt():
        if selected_file_path:
            password = simpledialog.askstring("Password", "Enter the password to decrypt:", show='*')
            if password:
                success = decrypt_file(selected_file_path, password)
                if success:
                    # Log the successful operation to the database!
                    log_operation("Decrypt", selected_file_path)
                    
                    messagebox.showinfo("Success", "Password accepted. File decrypted!")
                    file_status_label.configure(text="No file selected", text_color="gray")
                else:
                    messagebox.showerror("Error", "Incorrect password! Access denied.")
        else:
            messagebox.showerror("Error", "Please select a file first!")

    def view_history():
        # Connects to the database and fetches the 5 most recent actions
        conn = sqlite3.connect("file_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Timestamp, Operation_Type, File_Path FROM FileOperation ORDER BY Operation_ID DESC LIMIT 5")
        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo("History", "No file operations recorded yet.")
            return

        history_text = ""
        for row in records:
            # Formats the raw data into a readable string
            filename = os.path.basename(row[2])
            history_text += f"[{row[0]}] {row[1]}: {filename}\n\n"
        
        messagebox.showinfo("Recent Operations", history_text)

    file_status_label = ctk.CTkLabel(window, text="No file selected", text_color="gray")
    file_status_label.pack(pady=10)

    browse_button = ctk.CTkButton(window, text="Select File", command=browse_file, width=200, height=40)
    browse_button.pack(pady=10)
    
    encrypt_button = ctk.CTkButton(window, text="Encrypt File", command=gui_encrypt, width=200, height=40, fg_color="#28a745", hover_color="#218838")
    encrypt_button.pack(pady=10)
    
    decrypt_button = ctk.CTkButton(window, text="Decrypt File", command=gui_decrypt, width=200, height=40, fg_color="#dc3545", hover_color="#c82333")
    decrypt_button.pack(pady=10)

    # New button to view the SQLite logs
    history_button = ctk.CTkButton(window, text="View History", command=view_history, width=200, height=40, fg_color="#1f538d", hover_color="#14375e")
    history_button.pack(pady=10)

    copyright_label = ctk.CTkLabel(window, text="© 2026 Fuzail Ahmed. All Rights Reserved.", text_color="gray", font=("Arial", 10))
    copyright_label.pack(side="bottom", pady=10)

    window.mainloop()

start_gui()