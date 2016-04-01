import unittest
import socket
import sys

import webhttp.message
import webhttp.parser


portnr = 8001


class TestGetRequests(unittest.TestCase):
    """Test cases for GET requests"""

    def setUp(self):
        """Prepare for testing"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", portnr))
        self.parser = webhttp.parser.ResponseParser()

    def tearDown(self):
        """Clean up after testing"""
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()

    def test_existing_file(self):
        """GET for a single resource that exists"""
        # Send the request
        request = webhttp.message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request.set_header("Host", "localhost:{}".format(portnr))
        request.set_header("Connection", "close")
        self.client_socket.send(str(request))

        # Test response
        message = self.client_socket.recv(1024)
        response = self.parser.parse_response(message)
        self.assertEqual(response.code, 200)
        self.assertTrue(response.body)

    def test_nonexistant_file(self):
        """GET for a single resource that does not exist"""
        pass

    def test_caching(self):
        """GET for an existing single resource followed by a GET for that same
        resource with caching utilized on the client/tester side
        """
        pass

    def test_extisting_index_file(self):
        """GET for a directory with an existing index.html file"""
        pass

    def test_nonexistant_index_file(self):
        """GET for a directory with a non-existant index.html file"""
        pass

    def test_persistent_close(self):
        """Multiple GETs over the same (persistent) connection with the last
        GET prompting closing the connection, the connection should be closed.
        """
        pass

    def test_persistent_timeout(self):
        """Multiple GETs over the same (persistent) connection, followed by a
        wait during which the connection times out, the connection should be
        closed.
        """
        pass

    def test_encoding(self):
        """GET which requests an existing resource using gzip encodign, which
        is accepted by the server.
        """
        pass


if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Tests")
    parser.add_argument("-p", "--port", type=int, default=8001)
    
    # Arguments for the unittest framework
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    
    # Only pass the unittest arguments to unittest
    sys.argv[1:] = args.unittest_args

    # Start test suite
    unittest.main()
