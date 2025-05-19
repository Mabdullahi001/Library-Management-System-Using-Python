import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Muhammed2004",
        database="library_db"
    )

# Initialize database tables
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            member_id INT NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    ''')
    conn.commit()
    conn.close()

# GUI Application
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        # Left side - Display Screen
        self.display_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.display_frame.place(x=10, y=10, width=680, height=580)

        self.display_text = tk.Text(self.display_frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", fg="#333333")
        self.display_text.pack(fill=tk.BOTH, expand=True)

        # Right side - Buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.place(x=700, y=10, width=280, height=580)

        # Buttons
        self.add_book_btn = tk.Button(self.button_frame, text="Add Book", command=self.add_book, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_book_btn.pack(fill=tk.X, pady=5)

        self.search_book_btn = tk.Button(self.button_frame, text="Search Book", command=self.search_book, bg="#2196F3", fg="white", font=("Arial", 12))
        self.search_book_btn.pack(fill=tk.X, pady=5)

        self.update_book_btn = tk.Button(self.button_frame, text="Update Book", command=self.update_book, bg="#FF9800", fg="white", font=("Arial", 12))
        self.update_book_btn.pack(fill=tk.X, pady=5)

        self.delete_book_btn = tk.Button(self.button_frame, text="Delete Book", command=self.delete_book, bg="#F44336", fg="white", font=("Arial", 12))
        self.delete_book_btn.pack(fill=tk.X, pady=5)

        self.add_member_btn = tk.Button(self.button_frame, text="Add Member", command=self.add_member, bg="#9C27B0", fg="white", font=("Arial", 12))
        self.add_member_btn.pack(fill=tk.X, pady=5)

        self.borrow_book_btn = tk.Button(self.button_frame, text="Borrow Book", command=self.borrow_book, bg="#607D8B", fg="white", font=("Arial", 12))
        self.borrow_book_btn.pack(fill=tk.X, pady=5)

        self.return_book_btn = tk.Button(self.button_frame, text="Return Book", command=self.return_book, bg="#009688", fg="white", font=("Arial", 12))
        self.return_book_btn.pack(fill=tk.X, pady=5)

        self.view_logs_btn = tk.Button(self.button_frame, text="View Logs", command=self.view_logs, bg="#795548", fg="white", font=("Arial", 12))
        self.view_logs_btn.pack(fill=tk.X, pady=5)

        self.view_books_btn = tk.Button(self.button_frame, text="View Books", command=self.view_books, bg="#3F51B5", fg="white", font=("Arial", 12))
        self.view_books_btn.pack(fill=tk.X, pady=5)

        # New Button: View Members
        self.view_members_btn = tk.Button(self.button_frame, text="View Members", command=self.view_members, bg="#E91E63", fg="white", font=("Arial", 12))
        self.view_members_btn.pack(fill=tk.X, pady=5)

    def add_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Add Book Feature\n")

        # Create a new window for adding a book
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book")
        add_book_window.geometry("400x300")

        tk.Label(add_book_window, text="Title:", font=("Arial", 12)).pack(pady=5)
        title_entry = tk.Entry(add_book_window, font=("Arial", 12))
        title_entry.pack(pady=5)

        tk.Label(add_book_window, text="Author:", font=("Arial", 12)).pack(pady=5)
        author_entry = tk.Entry(add_book_window, font=("Arial", 12))
        author_entry.pack(pady=5)

        tk.Label(add_book_window, text="Quantity:", font=("Arial", 12)).pack(pady=5)
        quantity_entry = tk.Entry(add_book_window, font=("Arial", 12))
        quantity_entry.pack(pady=5)

        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            quantity = quantity_entry.get()

            if title and author and quantity:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)", (title, author, quantity))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book added successfully!")
                    add_book_window.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields!")

        tk.Button(add_book_window, text="Save", command=save_book, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

    def search_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Search Book Feature\n")

        # Create a new window for searching a book
        search_book_window = tk.Toplevel(self.root)
        search_book_window.title("Search Book")
        search_book_window.geometry("400x200")

        tk.Label(search_book_window, text="Enter Title:", font=("Arial", 12)).pack(pady=5)
        title_entry = tk.Entry(search_book_window, font=("Arial", 12))
        title_entry.pack(pady=5)

        def search():
            title = title_entry.get()
            if title:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{title}%",))
                books = cursor.fetchall()
                conn.close()

                self.display_text.delete(1.0, tk.END)
                if books:
                    for book in books:
                        self.display_text.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}\n")
                else:
                    self.display_text.insert(tk.END, "No books found!")
                search_book_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter a title!")

        tk.Button(search_book_window, text="Search", command=search, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

    def update_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Update Book Feature\n")

        # Create a new window for updating a book
        update_book_window = tk.Toplevel(self.root)
        update_book_window.title("Update Book")
        update_book_window.geometry("400x300")

        tk.Label(update_book_window, text="Book ID:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(update_book_window, font=("Arial", 12))
        id_entry.pack(pady=5)

        tk.Label(update_book_window, text="New Title:", font=("Arial", 12)).pack(pady=5)
        title_entry = tk.Entry(update_book_window, font=("Arial", 12))
        title_entry.pack(pady=5)

        tk.Label(update_book_window, text="New Author:", font=("Arial", 12)).pack(pady=5)
        author_entry = tk.Entry(update_book_window, font=("Arial", 12))
        author_entry.pack(pady=5)

        tk.Label(update_book_window, text="New Quantity:", font=("Arial", 12)).pack(pady=5)
        quantity_entry = tk.Entry(update_book_window, font=("Arial", 12))
        quantity_entry.pack(pady=5)

        def save_update():
            book_id = id_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            quantity = quantity_entry.get()

            if book_id and (title or author or quantity):
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    if title:
                        cursor.execute("UPDATE books SET title = %s WHERE id = %s", (title, book_id))
                    if author:
                        cursor.execute("UPDATE books SET author = %s WHERE id = %s", (author, book_id))
                    if quantity:
                        cursor.execute("UPDATE books SET quantity = %s WHERE id = %s", (quantity, book_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book updated successfully!")
                    update_book_window.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please fill at least one field!")

        tk.Button(update_book_window, text="Update", command=save_update, bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=10)

    def delete_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Delete Book Feature\n")

        # Create a new window for deleting a book
        delete_book_window = tk.Toplevel(self.root)
        delete_book_window.title("Delete Book")
        delete_book_window.geometry("400x200")

        tk.Label(delete_book_window, text="Book ID:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(delete_book_window, font=("Arial", 12))
        id_entry.pack(pady=5)

        def delete():
            book_id = id_entry.get()
            if book_id:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book deleted successfully!")
                    delete_book_window.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please enter a book ID!")

        tk.Button(delete_book_window, text="Delete", command=delete, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

    def add_member(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Add Member Feature\n")

        # Create a new window for adding a member
        add_member_window = tk.Toplevel(self.root)
        add_member_window.title("Add Member")
        add_member_window.geometry("400x300")

        tk.Label(add_member_window, text="Name:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(add_member_window, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(add_member_window, text="Email:", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(add_member_window, font=("Arial", 12))
        email_entry.pack(pady=5)

        def save_member():
            name = name_entry.get()
            email = email_entry.get()

            if name and email:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Member added successfully!")
                    add_member_window.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields!")

        tk.Button(add_member_window, text="Save", command=save_member, bg="#9C27B0", fg="white", font=("Arial", 12)).pack(pady=10)

    def borrow_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Borrow Book Feature\n")

        # Create a new window for borrowing a book
        borrow_book_window = tk.Toplevel(self.root)
        borrow_book_window.title("Borrow Book")
        borrow_book_window.geometry("400x300")

        tk.Label(borrow_book_window, text="Book ID:", font=("Arial", 12)).pack(pady=5)
        book_id_entry = tk.Entry(borrow_book_window, font=("Arial", 12))
        book_id_entry.pack(pady=5)

        tk.Label(borrow_book_window, text="Member ID:", font=("Arial", 12)).pack(pady=5)
        member_id_entry = tk.Entry(borrow_book_window, font=("Arial", 12))
        member_id_entry.pack(pady=5)

        def borrow():
            book_id = book_id_entry.get()
            member_id = member_id_entry.get()

            if book_id and member_id:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Check if the book is available
                    cursor.execute("SELECT quantity FROM books WHERE id = %s", (book_id,))
                    result = cursor.fetchone()
                    if result and result[0] > 0:
                        # Insert into transactions table
                        cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)", (book_id, member_id, datetime.now().date()))
                        # Decrease the book quantity
                        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Book borrowed successfully!")
                        borrow_book_window.destroy()
                    else:
                        messagebox.showwarning("Error", "Book not available!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields!")

        tk.Button(borrow_book_window, text="Borrow", command=borrow, bg="#607D8B", fg="white", font=("Arial", 12)).pack(pady=10)

    def return_book(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "Return Book Feature\n")

        # Create a new window for returning a book
        return_book_window = tk.Toplevel(self.root)
        return_book_window.title("Return Book")
        return_book_window.geometry("400x300")

        tk.Label(return_book_window, text="Transaction ID:", font=("Arial", 12)).pack(pady=5)
        transaction_id_entry = tk.Entry(return_book_window, font=("Arial", 12))
        transaction_id_entry.pack(pady=5)

        def return_book_func():
            transaction_id = transaction_id_entry.get()

            if transaction_id:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Get book_id from the transaction
                    cursor.execute("SELECT book_id FROM transactions WHERE id = %s", (transaction_id,))
                    result = cursor.fetchone()
                    if result:
                        book_id = result[0]
                        # Update the return date in the transactions table
                        cursor.execute("UPDATE transactions SET return_date = %s WHERE id = %s", (datetime.now().date(), transaction_id))
                        # Increase the book quantity
                        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Book returned successfully!")
                        return_book_window.destroy()
                    else:
                        messagebox.showwarning("Error", "Invalid transaction ID!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please enter a transaction ID!")

        tk.Button(return_book_window, text="Return", command=return_book_func, bg="#009688", fg="white", font=("Arial", 12)).pack(pady=10)

    def view_logs(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "View Logs Feature\n")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions")
            logs = cursor.fetchall()
            conn.close()

            if logs:
                self.display_text.insert(tk.END, "Transaction Logs:\n\n")
                for log in logs:
                    self.display_text.insert(tk.END, f"Transaction ID: {log[0]}\nBook ID: {log[1]}\nMember ID: {log[2]}\nIssue Date: {log[3]}\nReturn Date: {log[4]}\n\n")
            else:
                self.display_text.insert(tk.END, "No transaction logs found!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def view_books(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "View Books Feature\n")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            conn.close()

            if books:
                self.display_text.insert(tk.END, "List of Books:\n\n")
                for book in books:
                    self.display_text.insert(tk.END, f"ID: {book[0]}\nTitle: {book[1]}\nAuthor: {book[2]}\nQuantity: {book[3]}\n\n")
            else:
                self.display_text.insert(tk.END, "No books found in the database!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # New Function: View Members
    def view_members(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "View Members Feature\n")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            members = cursor.fetchall()
            conn.close()

            if members:
                self.display_text.insert(tk.END, "List of Members:\n\n")
                for member in members:
                    self.display_text.insert(tk.END, f"ID: {member[0]}\nName: {member[1]}\nEmail: {member[2]}\n\n")
            else:
                self.display_text.insert(tk.END, "No members found in the database!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

# Main function
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()