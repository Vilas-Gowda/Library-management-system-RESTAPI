import sqlite3

conn = sqlite3.connect("users.sqlite")
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

query3 = """
INSERT INTO admin(username, password) values("admin2","admin123")
"""

query4 = "DROP TABLE admin"
query5 = "DROP TABLE users"

#cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
#cursor.execute(query4)
#cursor.execute(query5)


conn.commit()
conn.close()