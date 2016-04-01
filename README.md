# Project 1 HTTP Server Framework

## Description

This repo contains a framework for the first project.
It provides a class structure and several utility wrappers for the Python Standard Library (so that you don't have to dig in the Python Docs).
The project can be completed by filling in the empty methods

## File Structure

* proj_sn1_sn2
    * content
        * test
            * index.html
    * webhttp
        * composer.py
        * \_\_init\_\_.py
        * message.py
        * resource.py
        * parser.py
        * server.py
    * webserver.py
    * webtests.py

The content directory contains the content for the website.
The test subfolder is meant for resources that are used by the tests which are defined in webtests.py.

The webhttp directory contains a package for HTTP.
Most methods are unimplemented.
The file message.py contains classes for HTTP messages.
The base class Message implements a basic HTTP message, which is specialized by Request and Response, which are for HTTP requests and HTTP responses respectively.
The file resource.py contains a handler class for resources.
The file parser.py contains classes for parsing HTTP requests and responses.
The file composer.py contains a class for composing responses to request.
The file server.py contains the main HTTP server.

The webserver.py file is Python file for starting the HTTP server, this file is fully implemented.

Finally webtests.py contains the tests for your HTTP server.
You manually have to start the HTTP server before running the tests.
Currently only one of the tests is implemented, you will have to implement the other tests.

## Suggested Implementation Order

1. Implement "run" in the class "Server" in "webhttp/server.py". This method should listen for incoming connections and create to a "ConnectionHandler" to handle the connection.
2. Implement "handle_connection" in the class "ConnectionHandler" in "webhttp/server.py". For now this method should receive a response from a client, send "Hello World" back and close the connection. Test that this works using the Python shell.
3. Implement "parse_requests" in the class "RequestParser" in "webhttp/parser.py". You can test your implementation by using to parse a few Requests in the Python shell.
4. Implement "\_\_str\_\_" for "Message", "Response" and "Request" in "webhttp/message.py". This function should return a string representation of the message according to the RFC. In order to test this you should create a few Responses and Requests in the Python shell and test if they comply with the RFC.
5. Reimplement "handle_connection" using "Response", "Request", "RequestParser" and "ResponseComposer".
6. Implement "parse_response" in "ResponseParser" in "webhttp/parser.py". At this point you should be able to pass the test in "webtests.py".
7. Replace the stub code in "compose_response" in "ResponseComposer" in "webhttp/composer.py". The composer should now be able to create the correct response to a request. You can ignore persistent connections and client side caching for now, but the response should have the right code and body.
8. Write additional tests in "webtests.py" for the following scenarios:
    * GET for a single resource that does not exist
    * GET for a directory with an existing index.html file
    * GET for a directory with non-existing index.html file
Your code should be able to pass these tests at this point.
9. Implement client side caching using ETags in "compose_response" and "generate_etag" in the class "Resource" in "resource.py". The "os.stat" module might be useful for generating an ETag. You should also implement the following test (which your server should pass at this point):
    * GET for an existing resource followed by a GET for that same resource, with caching utilized on the client/tester side.
10. Implement persistent connections in "compose_response" and "handle_connection", and implement the following tests:
    * multiple GETs over the same (persistent) connection with the last GET prompting closing the connection, the connection should be closed.
    * multiple GETs over the same (persistent) connection, followed by a wait during which the connection times out, the connection should be closed.
11. Implement content encoding. You may need to add extra methods to class "Resource" for this. You should also implement the following test:
    * GET which requests an existing resource gzip encoding, which is accepted by the server.
