# 🔒 Secure File Encryption Tool

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet?style=for-the-badge)
![Cryptography](https://img.shields.io/badge/Security-Fernet_AES-green?style=for-the-badge)
![Copyright](https://img.shields.io/badge/Copyright-%C2%A9_2026_Fuzail_Ahmed-red?style=for-the-badge)

A modern, lightweight desktop application built with Python that allows you to securely encrypt and decrypt your sensitive files. Featuring a clean dark-mode interface and local SQLite logging, this tool ensures your data remains safe and your encryption history stays organized.

---

## ✨ Features

- **Robust Security:** Uses `cryptography` (PBKDF2HMAC + SHA256) to derive secure keys and Fernet (AES) for file-level encryption.
- **Modern Interface:** Built with `customtkinter` for a sleek, responsive, and intuitive dark-themed user experience.
- **History Tracking:** Automatically logs encryption and decryption actions to a local SQLite database (`file_history.db`).
- **In-App History Viewer:** Instantly view your 5 most recent file operations directly from the GUI.
- **Standalone Ready:** Pre-configured `main.spec` file included for easy packaging into a standalone `.exe` using PyInstaller.

---

## 📸 Screenshots

*(Add a screenshot of your application here to make your repository stand out!)*
> `![App Interface](link-to-your-image.png)`

---

## 🚀 Installation & Setup

### Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/thefuzailahmed/secure-file-encryption-tool.git
cd secure-file-encryption-tool
```

### 2. Install Dependencies
Install the required Python libraries using pip:
```bash
pip install customtkinter cryptography
```

### 3. Run the Application
Launch the tool directly via Python:
```bash
python main.py
```

---

## 💻 How to Use

1. **Select a File:** Click the "Select File" button and browse for the file you want to protect.
2. **Encrypt:** Click "Encrypt File", enter a strong password, and the file will be secured and renamed with an `.encrypted` extension.
3. **Decrypt:** Select an `.encrypted` file, click "Decrypt File", enter the correct password, and your original file will be restored.
4. **View Logs:** Click "View History" to see a timestamped log of your recent activity.

> ⚠️ **IMPORTANT WARNING:** 
> There is no "forgot password" feature. If you lose the password used to encrypt a file, that file **cannot be recovered**.

---

## 📦 Building an Executable (.exe)

If you want to share this tool as a standalone application without requiring Python to be installed, you can build it using PyInstaller and the provided `main.spec` file:

```bash
pip install pyinstaller
pyinstaller main.spec
```
The compiled executable will be located in the newly created `dist/` folder.

---

## ⚖️ Copyright & License

**© 2026 Fuzail Ahmed. All Rights Reserved.**

This software and its source code may not be copied, modified, or distributed without express permission from the author.