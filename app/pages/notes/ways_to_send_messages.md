title: ways to send messages
date: 2017-06-24 12:00:00
published: false
type: notes

There are three ways to send messages between the browser and the web app server:
1- post or get requests
2- ajax
3- sockets

#1- http requests
the browser (triggered by a user action) requests something from the server (usually sends some information - what it wants or user entered data etc - and asks for something back - info from the server or confirmation received)

the whole page is reloaded when the reply is sent back from the server

types of requests:
POST
GET


#2- ajax
this uses a http request but it doesn't reload the page. the response from the server is sent back as json (or xml? - check), and the browser adds this to the page via javascript

#3- sockets
this is different from a http request (uses a http header though?) - it is a different protocol built on tcp
once a socket is open between client and server info can constantly be sent
