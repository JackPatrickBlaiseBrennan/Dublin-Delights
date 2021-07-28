#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = '<p>You are already logged out</p>'
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=True)
            session_store['authenticated'] = False
            session_store.close()
            result = """
                <p>You are now logged out.</p>
                """
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
                        <li><a href = "Login.py">Login</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <section id = "initial">
                        %s
                </section>
            </main>
        </body>
    </html>""" % (result))
