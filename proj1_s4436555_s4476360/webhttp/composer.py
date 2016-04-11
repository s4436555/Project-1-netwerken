""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

import webhttp.message
import webhttp.resource

accept_enc = {
    "gzip",
    "identity",
    "*"
}

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
        if request.get_header("Connection") != "keep-alive":
            self.persistent = False
        
        if request.get_version() == "HTTP/1.1":
            try:
                resource = webhttp.resource.Resource(request.uri)
                etag = resource.generate_etag()
                if self.match_etag(etag, request):
                    response = self.compose_common()
                    response.code = 304
                else:
                    encoding = request.get_header("Accept-Encoding")
                    prefencoding = self.find_preferred_encoding(encoding)
                    if prefencoding != "none":
                        response = self.compose_common()
                        response.code = 200
                        response.set_header("ETag", etag)
                        response.set_header("Content-Type", resource.get_content_type())
                        resource.encode_content(prefencoding)
                        response.set_header("Content-Length", resource.get_content_length())
                        response.set_header("Content-Encoding", resource.get_content_encoding())
                        response.body = resource.get_content()
                    else:
                        response = self.compose_error(406, True, False)
            except webhttp.resource.FileExistError:
                response = self.compose_error(404, True, False)
            except webhttp.resource.FileAccessError:
                response = self.compose_error(403, True, False)
        else:
            response = self.compose_error(505, True, False)
            
        if not self.persistent:
            response.set_header("Connection", "close")

        return response
    
    def compose_common(self):
        response = webhttp.message.Response()
        response.set_header("Date", self.make_date_string())
        
        return response
    
    def compose_error(self, code, body, close):
        response = self.compose_common()
        
        response.code = code
        if body:
            response.body = "<b>{}</b> {}".format(
                code, webhttp.message.reasondict[code]
            )
            response.set_header("Content-Type", "text/html")
            response.set_header("Content-Length", len(response.body))
        if close:
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
        def encoding_tuple(encstr):
            parts = encstr.split(";")
            if len(parts) > 1:
                q_pos = parts[1].find("q=")
                if q_pos >= 0:
                    q_part = parts[1][q_pos+2:len(parts[1])]
                    try:
                        q = float(q_part)
                    except ValueError:
                        print("Failed to parse: " + q_part)
                        q = 1.0
            else:
                q = 1.0
            return (parts[0], q)
        
        if encoding == "":
            return "identity"
        
        encodings = [encoding_tuple(enc) for enc in encoding.split(", ")]
        for (enc, q) in sorted(encodings, key = lambda enc: enc[1]):
            if enc in accept_enc:
                if q > 0:
                    return enc
                else:
                    if enc == "identity" or enc == "*":
                        return "none"
            
        return "identity"
        
    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
