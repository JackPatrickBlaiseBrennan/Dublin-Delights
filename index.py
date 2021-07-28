#!/usr/local/bin/python3

from cgitb import enable
enable()
from os import environ
from cgi import FieldStorage
from html import escape
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

print('Content-Type: text/html')
print()

form_data = FieldStorage()
form = """  <form id ="searcher">
                <label for="airport">AIRPORT CODE :</label>
                <select id="airport">
                  <option value="">Any</option>
                </select>
                <label for="depart">DEPARTURE :</label>
                <input type="date" name="depart" id="depart" />
                <input type="submit" value="Get" />
            </form>"""
result = ""
login = "Login"
userpage = ""
user = ""
dest = escape(form_data.getfirst('dest', '').strip())
price = int(escape(form_data.getfirst('price', '0').strip()))
airline = escape(form_data.getfirst('airline', '').strip())
flight_number = int(escape(form_data.getfirst('flight_number', '0').strip()))
departure_at = escape(form_data.getfirst('departure_at', '').strip().replace("T"," ").replace("Z", ""))
return_at = escape(form_data.getfirst('return_at', '').strip().replace("T"," ").replace("Z", ""))

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                userpage = """<li><a href = "userpage.py">Userpage</a></li>"""
                login = "Logout"
                user = """<p>Welcome back %s!</p>""" % session_store.get('username')
                if len(form_data) != 0:
                    username = escape(session_store.get('username').strip())
                    try:
                        connection = db.connect('localhost', 'username', 'password', 'db')
                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""INSERT INTO user_fav (username, dest, price, airline, flight_number, departs, returns)
                                          VALUES (%s, %s,%s,%s,%s,%s,%s);""", (username, dest, price, airline, flight_number, departure_at, return_at))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        result = """
                           <p>Succesfully inserted!</p>
                           """
                        form = ""
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
        <script src="flight.js" type="module"></script>
    </head>
    <body>
        <header>
            <h1>Flights from Dublin</h1>
            <nav>
                <ul>
                    <li><a href = "">Home</a></li>
                    %s
                    <li><a id ="login" href = "%s.py">%s</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id = "initial">
                %s
                %s
                %s
            </section>
        </main>
    </body>
</html>""" % (userpage, login, login, user,result, form))
