#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
login = 'Login'
userpage = ''
username = ''
result = ''
form = """  <form action="Login.py" method="post">
                <label for="username">User name: </label>
                <input type="text" name="username" id="username" value="" />
                <label for="password">Password: </label>
                <input type="password" name="password" id="password" />
                <input type="submit" value="Login" />
            </form>
            <a href="register.py">Not a user yet? Click here to <b>register</b></a>"""

if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    form = """  <form action="Login.py" method="post">
                    <label for="username">User name: </label>
                    <input type="text" name="username" id="username" value="%s" />
                    <label for="password">Password: </label>
                    <input type="password" name="password" id="password" />
                    <input type="submit" value="Login" />
                </form>
                <a href="register.py">Not a user yet? Click here to <b>register</b></a>""" % (username)
    if not username or not password:
        result = '<p>Error: user name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('localhost', 'username', 'password', 'db')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Error: incorrect user name or password</p>'
            else:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                login = "Logout"
                userpage = """<li><a href = "userpage.py">Userpage</a></li>"""
                result = """<p>Succesfully logged in!</p>
                            <p>Welcome back %s!</p>""" % username
                form = ""
                print(cookie)
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()

try:
    cookie_check = SimpleCookie()
    http_cookiecheck_header = environ.get('HTTP_COOKIE')
    if http_cookiecheck_header:
        cookie_check.load(http_cookiecheck_header)
        if 'sid' in cookie_check:
            sid = cookie_check['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                form = """<p>Hey, %s. Your already logged in!</p>""" % session_store.get('username')
                userpage = """<li><a href = "userpage.py">Userpage</a></li>"""
                login = "Logout"
            session_store.close()
except IOError:
    form = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="flight.css">
            <title>Dublin Delights</title>
        </head>
        <body>
            <header>
                <h1>Flights from Dublin</h1>
                <nav>
                    <ul>
                        <li><a href = "index.py">Home</a></li>
                        %s
                        <li><a href = "%s.py">%s</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <section id = "initial">
                %s
                %s
                </section>
            </main>
        </body>
    </html>""" % (userpage, login, login, form, result))
