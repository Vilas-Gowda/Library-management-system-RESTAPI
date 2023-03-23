import sqlite3

conn = sqlite3.connect("tables.sqlite")
cursor = conn.cursor()

query1 = """
CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL
    )
"""
query2 = """
CREATE TABLE admin (
    adminid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL
    )
"""
query31 = """
INSERT INTO users (username, password, email) values("demo","demo123","demo@gmail.com")
"""
query3 = """
INSERT INTO admin(username, password, email) values("admin","admin123","admin@gmail.com")
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
    releasedate text NOT NULL,
    no_of_copies int NOT NULL
)
"""

query8 = """
INSERT INTO books (name, ISBN, author, releasedate, no_of_copies) values ("Harry Potter and the Philosopher's Stone", 9780747532743, "J.K Rowling", "FEB 2002", 10)
"""

#cursor.execute(query7)
#cursor.execute(query8)


query9 = """
CREATE TABLE lending (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookid INTEGER REFERENCES books(bookid),
    userid INTEGER REFERENCES users(userid),
    borrowdate text NOT NULL,
    returnbefore text NOT NULL
)
"""


cursor.execute(query9)
conn.commit()
conn.close()