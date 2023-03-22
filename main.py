from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import sqlite3
import secrets


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


class guestbooks(Resource):
    
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid,name FROM books")

        booklist = [ 
            dict( id = row[0], name = row[1]) for row in cursor.fetchall()
        ]
        conn.close()
        
        if booklist is not None:
            return jsonify(booklist)
        else:
            return "no books in the library", 404

class guestbook(Resource):
     
    def get(self, id):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name FROM books WHERE bookid =?",(id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            book = [dict(id = row[0], name = row[1])]
            return jsonify(book)
        else:
            return f"No book with id {id} found", 404

class guestregister(Resource):
    
    def post(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        username = request.headers.get("username")
        if username:
            password = secrets.token_urlsafe(16)
            cursor.execute("INSERT INTO users (username, password) values (?,?)",(username,password))
            conn.commit()
            conn.close()
            return jsonify([{"username": username, "password":password}])
        
    
class books(Resource):

    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate FROM books")

        booklist = [ 
            dict( id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4]) for row in cursor.fetchall()
        ]
        conn.close()
        
        if booklist is not None:
            return jsonify(booklist)
        else:
            return "no books in the library", 404
    
class book(Resource):

    def get(self, id):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate FROM books WHERE bookid =?",(id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            book = [dict(id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4])]
            return jsonify(book)
        else:
            return f"No book with id {id} found", 404

class authors(Resource):

    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT author FROM books")
        row = cursor.fetchall()
        conn.close()

        authorlist = [ 
            dict( authorname = row[0]) for row in cursor.fetchall()
        ]
        conn.close()
        
        if authorlist is not None:
            return jsonify(authorlist)
        else:
            return "no books in the library", 404
        
class book(Resource):

    def get(self, name):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate FROM books WHERE bookid =?",(id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            book = [dict(id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4])]
            return jsonify(book)
        else:
            return f"No book with id {id} found", 404

      



api.add_resource(guestregister,'/register')
api.add_resource(guestbooks, '/guest/books')
api.add_resource(guestbook, '/guest/book/<int:id>')













@auth.verify_password
def authenticate(username, password):
    conn = sqlite3.connect("tables.sqlite")
    cursor = conn.cursor()
    
    cursor = cursor.execute("SELECT password FROM users WHERE username=?",(username,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0] == password:
        return True
    else:
        return False
    
if __name__ == '__main__':
    app.run(debug = True)