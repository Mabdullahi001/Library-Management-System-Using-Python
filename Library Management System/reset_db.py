import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this if you have a different username
    password="@Muhammed2004"  # Replace with your actual MySQL password
)
cursor = conn.cursor()

# Drop and recreate the database
cursor.execute("DROP DATABASE IF EXISTS library_db")
cursor.execute("CREATE DATABASE library_db")

print("Database reset successfully!")

# Close connection
cursor.close()
conn.close()
