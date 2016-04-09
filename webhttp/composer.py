""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

import webhttp.message
import webhttp.resource


class ResponseComposer:
    """Class that composes a HTTP response to a HTTP request"""

    def __init__(self, timeout):
        """Initialize the ResponseComposer
        
        Args:
            timeout (int): connection timeout
        """
        self.timeout = timeout
    
    def compose_response(self, request):
        """Compose a response to a request
        
        Args:
            request (webhttp.Request): request from client

        Returns:
            webhttp.Response: response to request

        """
        response = webhttp.message.Response()
        
        try:
            resource = webhttp.resource.Resource(request.uri)
            response.code = 200
            response.set_header("Content-Length", resource.get_content_length())
            response.body = resource.get_content()
        except webhttp.resource.FileExistError:
            response.code = 404
            response.set_header("Content-Length", 20)
            response.body = "<b>404</b> Not Found"
        except webhttp.resource.FileAccessError:
            response.code = 403
            response.set_header("Content-Length", 28)
            response.body = "<b>403</b> Permission denied"
            
        response.set_header("Connection", "close")

        return response

    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
