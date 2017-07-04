title: python servers
date: 2017-05-30 12:00:00
published: false
type: notes

# What is a server?
It is a system that waits for a request to be sent to it.  It gets requests from clients (eg a browser).  Depending on the request and the server, the way it responds can be determined by scripts hosted on the server.  It sends something back to the client, and then keeps waiting. 

Servers have to be good at scaling up and down (to deal with different volumes of requests).  They have to respond reliably, and deal with clients that do not (eg. because someone is requesting a web page over a bad internet connection).

If the request is for a dynamic webpage on a webapp, the server also has to interact with the scripts which serve stuff to it to send back.  If a framework is used for the webapp, the framework has to be able to interact with the server on which it is hosted. 


# What is WSGI?
A protocol that defines how python programs and servers should interact.  This means any python framework can use any python server; before WSGI the choice of server was limited by the framework used.
WSGI has two sets of rules - one for the server and one for the framework.  The rules state what information each must make available, what layout or interface to expect from the other, and what to do incase something goes wrong.


# What is gunicorn and why use it with flask?
Gunicorn is a python server that uses WSGI.  It uses 'workers' to handle requests, so it can handle multiple requests at one time.  Flask's built in server processes each request one at a time; it works great for development, but for deployment it doesn't handle much traffic well.

To use gunicorn with a flask app:
1 - pip install gunicorn
2 - gunicorn <application>:<application-object> eg gunicorn app:app - the --log-file flag logs to the terminal

# For later:
flask, gunicorn, nginx stack how to: http://www.philchen.com/2015/08/08/how-to-make-a-scalable-python-web-app-using-flask-and-gunicorn-nginx-on-ubuntu-14-04
wsgi docs: http://wsgi.readthedocs.io/en/latest/
wsgi intro: http://ivory.idyll.org/articles/wsgi-intro/what-is-wsgi.html
