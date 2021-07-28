#!/usr/local/bin/python3

from cgitb import enable
enable()
from cgi import FieldStorage
from os import environ
from shelve import open
from http.cookies import SimpleCookie
from html import escape
import pymysql as db
form_data = FieldStorage()

print('Content-Type: text/html')
print()

nice = ["Price : ","Airline : ", "Flight Number : ", "Departs : ", "Returns : "]
login = 'Login'
result = """<section>
                <p>Not registered? Register to save the flights your most interested in to your account! Or log in to view your flights below.</p>
                <ul>
                    <li><a href="register.py">Register</a></li>
                    <li><a href="Login.py">Login</a></li>
                </ul>
            </section>"""

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                username = escape(session_store.get('username').strip())
                result = """<section id="initial">
                                <p>Hey, %s. Below are your saved flights!</p>
                                <a href = "userpage.py">Toggle Delete</a>
                            </section>""" % session_store.get('username')
                login = 'Logout'
                try:
                    connection = db.connect('localhost', 'username', 'password', 'db')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    if len(form_data) != 0:
                        id = escape(form_data.getfirst('id', '').strip())
                        cursor.execute("""DELETE FROM user_fav
                                          WHERE id = %s;""", (id))
                        connection.commit();
                        result = "<section><p>Succesfully Deleted</p></setion>"
                    else:
                        cursor.execute("""SELECT *
                                          FROM user_fav
                                          WHERE username = %s;""", (username))
                        for each in cursor.fetchall():
                            result += """<section>
                                            <h1>%s</h1>
                                            <p>%s%d</p>
                                            <p>%s%s</p>
                                            <p>%s%i</p>
                                            <p>%s%s</p>
                                            <p>%s%s</p>
                                            <form action="remove.py" method="post" target="_blank">
                                                <input name="id" type="text" id="dest" size="5" class="disabled" value="%s">
                                                <input type="submit" value="Delete">
                                            </form>
                                        </section>""" % (each['dest'], nice[0], each['price'], nice[1], each['airline'],nice[2], each['flight_number'],nice[3], each['departs'],nice[4], each['returns'], each['id'])
                    cursor.close()
                    connection.close()
                except (db.Error, IOError):
                    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
            session_store.close()
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Dublin Delights</title>
            <link rel="stylesheet" href="flight.css">
        </head>
        <body>
            <header>
                <h1>Flights from Dublin</h1>
                <nav>
                    <ul>
                        <li><a href = "index.py">Home</a></li>
                        <li><a href = "%s.py">%s</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                %s
            </main>
        </body>
    </html>""" % (login, login, result))
