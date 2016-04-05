"""HTTP Server

This module contains a HTTP server
"""

import threading
import socket
import webhttp.parser
import webhttp.composer

class ConnectionHandler(threading.Thread):
    """Connection Handler for HTTP Server"""

    def __init__(self, conn_socket, addr, timeout):
        """Initialize the HTTP Connection Handler
        
        Args:
            conn_socket (socket): socket used for connection with client
            addr (str): ip address of client
            timeout (int): seconds until timeout
        """
        super(ConnectionHandler, self).__init__()
        self.daemon = True
        self.conn_socket = conn_socket
        self.addr = addr
        self.timeout = timeout
    
    def handle_connection(self):
        """Handle a new connection"""
        
        parser = webhttp.parser.RequestParser()
        composer = webhttp.composer.ResponseComposer(self.timeout)
        
        request_buf = self.conn_socket.recv(4096)
        requests = parser.parse_requests(request_buf)
        
        for request in requests:
            self.conn_socket.send(str(composer.compose_response(request)))
        
        self.conn_socket.close()
        
    def run(self):
        """Run the thread of the connection handler"""
        print 'ConnectionHandler.run()'
        self.handle_connection()
        

class Server:
    """HTTP Server"""

    def __init__(self, hostname, server_port, timeout):
        """Initialize the HTTP server
        
        Args:
            hostname (str): hostname of the server
            server_port (int): port that the server is listening on
            timeout (int): seconds until timeout
        """
        self.hostname = hostname
        self.server_port = server_port
        self.timeout = timeout
        self.done = False
    
    def run(self):
        """Run the HTTP Server and start listening"""
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.hostname, self.server_port))
        self.serverSocket.listen(1)
        while not self.done:
            conn_socket, addr = self.serverSocket.accept()
            handler = ConnectionHandler(conn_socket, addr, self.timeout)
            handler.run()
    
    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
        self.serverSocket.close()
