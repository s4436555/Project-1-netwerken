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
        self.persistent = True
    
    def compose_response(self, request):
        """Compose a response to a request
        
        Args:
            request (webhttp.Request): request from client

        Returns:
            webhttp.Response: response to request

        """
        response = webhttp.message.Response()
        response.set_header("Date", self.make_date_string())
        
        if request.get_header("Connection") != "keep-alive":
            self.persistent = False
        
        try:
            resource = webhttp.resource.Resource(request.uri)
            etag = resource.generate_etag()
            if self.match_etag(etag, request):
                response.code = 304
            else:
                encoding = request.get_header("Accept-Encoding")
                prefencoding = self.find_preferred_encoding(encoding)
                if prefencoding == 2:
                    response.code = 200
                    response.set_header("ETag", etag)
                    response.set_header("Content-Encoding", "gzip")
                    response.body = resource.get_content()
                elif prefencoding == 1:
                    response.code = 200
                    response.set_header("ETag", etag)
                    response.set_header("Content-Length", resource.get_content_length())
                    response.body = resource.get_content()
                else:
                    response.code = 406
                    response.set_header("Content-Length", 25)
                    response.body = "<b>406</b> Not Acceptable"
        except webhttp.resource.FileExistError:
            response.code = 404
            response.set_header("Content-Length", 20)
            response.body = "<b>404</b> Not Found"
        except webhttp.resource.FileAccessError:
            response.code = 403
            response.set_header("Content-Length", 28)
            response.body = "<b>403</b> Permission denied"
            
        if not self.persistent:
            response.set_header("Connection", "close")

        return response

    def get_persistent(self):
        return self.persistent

    def match_etag(self, etag, request):
        resp_etags = request.get_header("If-None-Match")
        for resp_etag in resp_etags.split(", "):
            if resp_etag == etag:
                return True
        return False

    def find_preferred_encoding(self, encoding):
        qgzip = -1
        if "gzip" in encoding:
            qgzip = 1
        if "gzip;q=" in encoding:
            safeencoding = encoding + ","
            qgzip = float(encoding[encoding.find("gzip;q=")+7:safeencoding.find(",", encoding.find("gzip;q="))])
        qid = -1
        if "identity" in encoding:
            qid = 1
        if "identity;q=" in encoding:
            safeencoding = encoding + ","
            qid = float(encoding[encoding.find("identity;q=")+11:safeencoding.find(",", encoding.find("identity;q="))])
        qstar = 0
        if "*;q=" in encoding:
            safeencoding = encoding + ","
            qstar = float(encoding[encoding.find("*;q=")+4:safeencoding.find(",", encoding.find("*;q="))])
        if qgzip == -1:
            qgzip = qstar
        if qid == -1:
            if "*;q=" in encoding:
                qid = qstar
            else:
                qid = 1
        if encoding == "":
            qid = 1
        
        if qgzip > qid:
            return 2
        elif qid > 0:
            return 1
        else:
            return 0
        
    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
