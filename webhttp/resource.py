"""Resources

This module contains a handler class for resources.
"""

import os
import errno
import mimetypes
import urlparse
import gzip
import shutil

class FileExistError(Exception):
    """Exception which is raised when file does not exist"""
    pass


class FileAccessError(Exception):
    """Exception which is raised when file exists, but cannot be accessed"""
    pass


class Resource:
    """Class for representing a Resource (file)"""

    def __init__(self, uri):
        """Initialize the resource"

        Raises:
            FileExistError: if resource does not exist
            FileAccessError: if resource exists, but cannot be accessed

        Args:
            uri (str): Uniform Resource Identifier
        """
        self.uri = uri
        out = urlparse.urlparse(uri)
        self.path = os.path.join("content", out.path.lstrip("/"))
        if os.path.isdir(self.path):
            self.path = os.path.join(self.path, "index.html")
        if not os.path.isfile(self.path):
            raise FileExistError
        if not os.access(self.path, os.R_OK):
            raise FileAccessError

    def generate_etag(self):
        """Generate the ETag for the resource

        Returns:
            str: ETag for the resource
        """
        stat = os.stat(self.path)
        etag = "\"{0:x}\"".format(int(stat.st_mtime * 100)) # should be precise enough
        return etag

    def get_content(self):
        """Get the contents of the resource
        
        Returns:
            str: Contents of the resource
        """
        return open(self.path).read()

    def get_content_type(self):
        """Get the content type, i.e "text/html"

        Returns:
            str: type of content in the resource
        """
        mimetype = mimetypes.guess_type(self.path)
        return mimetype[0]

    def encode_content(self, encoding):
        """Encodes the content of the path and stores it in a new file
        """
        if encoding == "gzip":
            new_path = os.path.join("temp", self.path.split("content")[1].lstrip("/")) 
            new_path = new_path + ".gz"
            new_path_dir = os.path.dirname(new_path)
            try:
                os.makedirs(new_path_dir)
            except OSError:
                if not os.path.isdir(new_path_dir):
                    raise
            with open(self.path, "rb") as f_in, gzip.open(new_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            self.path = new_path
    
    def get_content_encoding(self):
        """Get the content encoding, i.e "gzip"

        Returns:
            str: encoding used for the resource
        """
        mimetype = mimetypes.guess_type(self.path)
        return mimetype[1]

    def get_content_length(self):
        """Get the length of the resource

        Returns:
            int: length of resource in bytes
        """
        return os.path.getsize(self.path)
