from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import sqlite3
import secrets
import base64

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
        email = request.headers.get("email")
        if username and email:
            password = secrets.token_urlsafe(16)
            cursor.execute("INSERT INTO users (username, password, email) values (?,?,?)",(username, password, email))
            conn.commit()
            conn.close()
            return jsonify([{"username": username,"email":email, "password":password}])
        else:
            return "Headers missing", 404
    
class books(Resource):
    @auth.login_required
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate, no_of_copies FROM books")

        booklist = [ 
            dict( id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4], no_of_copies = row[5]) for row in cursor.fetchall()
        ]
        conn.close()
        
        if booklist is not None:
            return jsonify(booklist)
        else:
            return "no books in the library", 404
    
class book(Resource):
    @auth.login_required
    def get(self, id):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate, no_of_copies FROM books WHERE bookid =?",(id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            book = [dict(id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4], no_of_copies = row[5])]
            return jsonify(book)
        else:
            return f"No book with id {id} found", 404

class authors(Resource):
    @auth.login_required
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()

        cursor = cursor.execute("SELECT DISTINCT author FROM books")
        authorlist = [ 
            dict( authorname = row[0]) for row in cursor.fetchall()
        ]
        conn.close()
        
        if authorlist is not None:
            return jsonify(authorlist)
        else:
            return "no books in the library", 404
    
    
class author(Resource):
    @auth.login_required
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        author_name = request.headers.get("authorname")

        cursor = cursor.execute("SELECT bookid, name, ISBN, author, releasedate, no_of_copies FROM books WHERE author=?",(author_name,))
        booklist = [ 
            dict( id = row[0], name = row[1], ISBN = row[2], author = row[3], releasedate = row[4], no_of_copies = row[5]) for row in cursor.fetchall()
        ]
        conn.close()
        if booklist is not None:
            return jsonify(booklist)
        else:
            return f"no book with author {author_name} in the library", 404



class unregister(Resource):
    @auth.login_required
    def delete(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        username = request.headers.get("Username")
        if username:
            cursor.execute("DELETE FROM users WHERE username =?",(username,))
        else:
            return "Username header not included", 404
        conn.commit()
        conn.close()
        return "User unregistered from library", 200

class borrow(Resource):
    @auth.login_required
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        c = request.headers.get("Authorization")
        print(c)
        username =  c.split()[1]
        print(username)
        #username = str(base64.b64decode(c))
        #username = c.split(':')[0][2:]
        print(username)
        return "done"

api.add_resource(guestregister,'/register')
api.add_resource(guestbooks, '/guest/books')
api.add_resource(guestbook, '/guest/book/<int:id>')
api.add_resource(books, '/books')
api.add_resource(authors, '/authors')
api.add_resource(book, '/book/<int:id>')
api.add_resource(author, '/author')
api.add_resource(unregister, '/unregister')
api.add_resource(borrow, '/book/borrow')

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