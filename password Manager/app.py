import sqlite3
from cryptography.fernet import Fernet
import secrets
import string
import os
import sys
import time

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class PasswordManager:
    def __init__(self, db_file="passwords.db", key_file="secret.key"):
        self.db_file = db_file
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self._init_db()

    def _load_or_generate_key(self):
        """Load the encryption key or generate a new one if it doesn't exist."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as kf:
                return kf.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as kf:
                kf.write(key)
            return key

    def _init_db(self):
        """Initialize the database table."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password BLOB NOT NULL
                )
            ''')
            conn.commit()

    def _encrypt(self, password):
        """Encrypt a plaintext password."""
        f = Fernet(self.key)
        return f.encrypt(password.encode())

    def _decrypt(self, encrypted_password):
        """Decrypt an encrypted password."""
        f = Fernet(self.key)
        return f.decrypt(encrypted_password).decode()

    def add_password(self, site, username, password):
        """Add a new password entry."""
        encrypted_pwd = self._encrypt(password)
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
                    (site, username, encrypted_pwd)
                )
                conn.commit()
            print(f"✅ Password for '{site}' saved successfully.")
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")

    def get_password(self, site):
        """Retrieve a password for a specific site."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM passwords WHERE site LIKE ?", (site,))
            result = cursor.fetchone()
        
        if result:
            username, encrypted_pwd = result
            try:
                decrypted_pwd = self._decrypt(encrypted_pwd)
                return username, decrypted_pwd
            except Exception:
                print("❌ Error: Could not decrypt password. The key file may be mismatched.")
                return None
        else:
            return None

    def list_sites(self):
        """List all stored sites."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT site, username FROM passwords")
            results = cursor.fetchall()
        
        if not results:
            print("📭 No passwords stored yet.")
            return

        print("\n--- Stored Credentials ---")
        print(f"{'Site':<20} | {'Username':<20}")
        print("-" * 45)
        for site, username in results:
            print(f"{site:<20} | {username:<20}")
        print("-" * 45)

    def delete_password(self, site):
        """Delete a password entry."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE site LIKE ?", (site,))
            if cursor.rowcount > 0:
                print(f"🗑️ Entry for '{site}' deleted.")
            else:
                print(f"⚠️ No entry found for '{site}'.")
            conn.commit()

    @staticmethod
    def generate_random_password(length=16):
        """Generates a secure random password."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

# --- CLI Menu Functions ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = PasswordManager()
    
    while True:
        print("\n🔒 === PYTHON PASSWORD MANAGER === 🔒")
        print("1. Add New Password")
        print("2. Retrieve Password")
        print("3. List All Sites")
        print("4. Generate Random Password")
        print("5. Delete Password")
        print("Q. Quit")
        
        choice = input("\nSelect an option: ").lower().strip()

        if choice == '1':
            site = input("Enter Site Name (e.g., google.com): ")
            user = input("Enter Username: ")
            
            # Offer to generate password
            use_gen = input("Generate a random password? (y/n): ").lower()
            if use_gen == 'y':
                pwd = manager.generate_random_password()
                print(f"Generated Password: {pwd}")
            else:
                pwd = input("Enter Password: ")
            
            manager.add_password(site, user, pwd)

        elif choice == '2':
            site = input("Enter Site Name to search: ")
            cred = manager.get_password(site)
            if cred:
                user, pwd = cred
                print(f"\n✅ Found!")
                print(f"Site: {site}")
                print(f"User: {user}")
                print(f"Pass: {pwd}")
                
                if CLIPBOARD_AVAILABLE:
                    copy = input("Copy password to clipboard? (y/n): ").lower()
                    if copy == 'y':
                        pyperclip.copy(pwd)
                        print("📋 Password copied to clipboard!")
            else:
                print("❌ Site not found.")

        elif choice == '3':
            manager.list_sites()

        elif choice == '4':
            length = input("Enter length (default 16): ")
            length = int(length) if length.isdigit() else 16
            pwd = manager.generate_random_password(length)
            print(f"\n🔑 Generated: {pwd}")
            if CLIPBOARD_AVAILABLE:
                    pyperclip.copy(pwd)
                    print("(Copied to clipboard)")

        elif choice == '5':
            site = input("Enter Site Name to DELETE: ")
            confirm = input(f"⚠️ Are you sure you want to delete {site}? (yes/no): ")
            if confirm.lower() == 'yes':
                manager.delete_password(site)

        elif choice == 'q':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option, try again.")
        
        time.sleep(1) # Short pause before menu loop

if __name__ == "__main__":
    main()