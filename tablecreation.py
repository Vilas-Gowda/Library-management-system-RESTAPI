import sqlite3

conn = sqlite3.connect("tables.sqlite")
cursor = conn.cursor()

query1 = """
CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL
    )
"""
query2 = """
CREATE TABLE admin (
    adminid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL
    )
"""
query31 = """
INSERT INTO users (username, password) values("demo","demo123")
"""
query3 = """
INSERT INTO admin(username, password) values("admin","admin123")
"""

#cursor.execute(query1)
#cursor.execute(query2)
#cursor.execute(query3)


query7 = """
CREATE TABLE books (
    bookid INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    ISBN int NOT NULL,
    author text NOT NULL,
    releasedate text NOT NULL
)
"""

query8 = """
INSERT INTO books (name, ISBN, author, releasedate) values ("Harry Potter and the Philosopher's Stone", 9780747532743, "J.K Rowling", "FEB 2002")
"""

#cursor.execute(query7)
#cursor.execute(query8)

username = "demo"
cursor = cursor.execute("SELECT password FROM users WHERE username=?",(username,))
row = cursor.fetchone()
print(row[0])
conn.commit()
conn.close()