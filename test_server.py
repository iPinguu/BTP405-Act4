import http
import unittest
import requests
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

import http.client
import json
import threading

class Test_ServerEndpoint(unittest.TestCase):
    @classmethod # what is @classmethod
    def setUpClass(cls):
        cls.server_address = ("localhost", 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)

        cls.server_thread.daemon = True
        cls.server_thread.start()
    
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_Get_Method(self):
        
        # Connects to the server and sends a GET request    
        connection = http.client.HTTPConnection(*self.server_address) # http.client because were simulating a client connection
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode GET reponse
        data = response.read().decode()
        connection.close()

        # Check Response is valid (Response is expected)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, "OK")
        self.assertEqual(response.getheader('content-type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': "This is a GET request response"})
    
    def test_Post_method(self):
        postSentData = json.dumps({"message": "test"})
        
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('POST', '/', postSentData, headers={'Content-Type': 'application/json'})
        postResponse = connection.getresponse()

        data = postResponse.read().decode() 
        connection.close()
        
        self.assertEqual(postResponse.status, 200)
        self.assertEqual(postResponse.reason, "OK")
        self.assertEqual(postResponse.getheader('content-type'), 'application/json')

        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': {"message": "test"}})



        










if __name__ == "__main__":
    unittest.main()