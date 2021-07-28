#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db
from os import environ

form_data = FieldStorage()
username = ''
login = 'Login'
result = ''
userpage = ''
form = """  <form action="register.py" method="post">
                <label for="username">User name: </label>
                <input type="text" name="username" id="username" value="" />
                <label for="password1">Password: </label>
                <input type="password" name="password1" id="password1" />
                <label for="passwords2">Re-enter password: </label>
                <input type="password" name="password2" id="password2" />
                <input type="submit" value="Register" />
            </form>
            <a href="Login.py">Already a user? Click here to <b>login</b></a>"""

if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    form = """  <form action="register.py" method="post">
                    <label for="username">User name: </label>
                    <input type="text" name="username" id="username" value="%s" />
                    <label for="password1">Password: </label>
                    <input type="password" name="password1" id="password1" />
                    <label for="passwords2">Re-enter password: </label>
                    <input type="password" name="password2" id="password2" />
                    <input type="submit" value="Register" />
                </form>
                <a href="Login.py">Already a user? Click here to <b>login</b></a>""" % username
    if not username or not password1 or not password2:
        result = '<p>Error: user name and passwords are required</p>'
    elif password1 != password2:
        result = '<p>Error: passwords must be equal</p>'
    else:
        try:
            connection = db.connect('localhost', 'username', 'password', 'db')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                result = '<p>Error: user name already taken</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, password)
                                  VALUES (%s, %s)""", (username, sha256_password))
                connection.commit()
                cursor.close()
                connection.close()
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <p>Succesfully inserted! Thanks for joining! You are now logged in</p>
                   """
                userpage = """<li><a href = "userpage.py">Userpage</a></li>"""
                login = "Logout"
                form = ""
                print(cookie)
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
                form = """
                    <p>Hey, %s. Your already logged in!</p>
                    """ % session_store.get('username')
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
    </html>""" % (userpage,login, login, form, result))
