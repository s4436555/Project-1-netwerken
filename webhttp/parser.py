"""HTTP response and request parsers

This module contains parses for HTTP response and HTTP requests.
"""

import webhttp.message


class RequestParser:
    """Class that parses a HTTP request"""

    def __init__(self):
        """Initialize the RequestParser"""
        pass
        
    def parse_requests(self, buff):
        """Parse requests in a buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            list of webhttp.Request
        """
        requests = self.split_requests(buff)
        
        http_requests = []
        for request in requests:
            http_request = webhttp.message.Request()
            http_requests.append(http_request)
        
        return http_requests

    def split_requests(self, buff):
        """Split multiple requests
        
        Arguments:
            buff (str): the buffer contents received from socket

        Returns:
            list of str
        """
        requests = buff.split('\r\n\r\n')
        requests = filter(None, requests)
        requests = [r + '\r\n\r\n' for r in requests]
        requests = [r.lstrip() for r in requests]
        return requests


class ResponseParser:
    """Class that parses a HTTP response"""
    def __init__(self):
        """Initialize the ResponseParser"""
        pass

    def parse_response(self, buff):
        """Parse responses in buffer

        Args:
            buff (str): the buffer contents received from socket

        Returns:
            webhttp.Response
        """
        response = webhttp.message.Response()
        return response
