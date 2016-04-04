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
            length = len(request)
            
            """Parsing the first line of the header
            
            Syntax:
                Request-Line   = Method SP Request-URI SP HTTP-Version CRLF
            """
            end_line = request.find('\r\n', 0)
            line_parts = request[0:end_line].split(' ')
            http_request.method = line_parts[0]
            http_request.uri = line_parts[1]
            http_request.version = line_parts[2]
            start_line = end_line + 2
            
            """Parsing 'key: value' header lines"""
            while (start_line + 1 < length and
                   request[start_line] != '\r' and 
                   request[start_line + 1] != '\n'):
                end_line = request.find('\r\n', start_line)
                if end_line < 0:
                    print("missing clrf")
                    break
                colon = request.find(': ', start_line, end_line)
                http_request.set_header(
                    request[start_line:colon], 
                    request[colon+1:end_line].strip()
                )
                start_line = end_line + 2
            
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
