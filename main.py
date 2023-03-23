from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from datetime import date, timedelta
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
        username = auth.username()
        cursor.execute("DELETE FROM users WHERE username =?",(username,))
        conn.commit()
        conn.close()
        return "User unregistered from library", 200

class borrow(Resource):
    @auth.login_required
    def get(self, id):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        username = auth.username()
        a = cursor.execute("SELECT no_of_copies FROM books WHERE bookid=?",(id,))
        a=a.fetchone()
        if a is None:
            return f"Books with id {id} is not present in library", 404
        if a[0] < 1:
            return f"There are no more copies of Book {id} left, try again later", 200
        
        cursor.execute("UPDATE books SET no_of_copies = no_of_copies - 1 WHERE bookid =?",(id,))

        userid = cursor.execute("SELECT userid FROM users WHERE username = ?",(username,))
        userid = userid.fetchone()

        today = date.today()
        enddate = date.today() + timedelta(days=30)
        d1 = today.strftime("%d/%m/%Y")
        d2 = enddate.strftime("%d/%m/%Y")

        cursor.execute("INSERT INTO lending (userid, bookid, borrowdate, returnbefore) values (?,?,?,?)",(userid[0], id, d1, d2))
        conn.commit()
        conn.close()
        return f"You have succesfully borrowed book {id} and must return it before {d2}", 200


class returnbook(Resource):
    @auth.login_required
    def get(self,id):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        username = auth.username()

        userid = cursor.execute("SELECT userid FROM books WHERE username =?",(username,))
        userid = userid.fetchone()
        userid = userid[0]

        lendid = cursor.execute("SELECT id FROM lending WHERE userid = ? AND bookid = ?",(userid, id))
        lendid = lendid.fetchone()
        
        if lendid is None:
            return f"User {userid} hasn't borrowd book {id}", 200
        
        cursor.execute("DELETE FROM lending WHERE id=?",(lendid,))
        cursor.execute("UPDATE FROM books SET no_of_copies = no_of_copies + 1 WHERE bookid = ?",(id,))
        conn.commit()
        conn.close()

        return f"Book {id} has been succesfully returned to the library", 200


class mybooks(Resource):
    @auth.login_required
    def get(self):
        conn = sqlite3.connect("tables.sqlite")
        cursor = conn.cursor()
        username = auth.username()

        userid = cursor.execute("SELECT userid FROM users WHERE username =?",(username,))
        userid = userid.fetchone()
        userid = userid[0]

        lendlist = cursor.execute("SELECT id, userid, bookid, borrowdate, returnbefore FROM lending WHERE id = ?",(userid,))
        lendlist =[
            dict(lendid = row[0], Userid= row[1], bookid = row[2], borrowdate = row[3], returnbefore = row[4]) for row in lendlist.fetchall()
        ]
        if lendlist is not None:
            return jsonify(lendlist)
        else:
            return f"User {userid} has borrowed no books from the library", 200
        


api.add_resource(guestregister,'/register')
api.add_resource(guestbooks, '/guest/books')
api.add_resource(guestbook, '/guest/book/<int:id>')
api.add_resource(books, '/books')
api.add_resource(authors, '/authors')
api.add_resource(book, '/book/<int:id>')
api.add_resource(author, '/author')
api.add_resource(unregister, '/unregister')
api.add_resource(borrow, '/book/borrow/<int:id>')
api.add_resource(returnbook, '/book/return/<int:id>')
api.add_resource(mybooks, '/mybooks')

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