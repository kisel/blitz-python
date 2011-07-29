__author__="ghermeto"
__date__ ="$27/07/2011 23:23:17$"

import json
import http.client

class Error(Exception):
    """ Base error for Blitz api. """
    
    def __init__(self, error, reason):
        self.error = error
        self.reason = reason

class Client:
    """ Responsable for requests to Blitz RESTful API """
    
    def __init__(self, user, api_key, host=None, port=None, connect=True):
        self.username = user
        self.api_key = api_key
        self.host = 'blitz.io' if host is None else host
        self.port = 80 if port is None else port
        self.private_key = None
        if connect:
            self.connect()
    
    def connect(self):
        """ Connects the client. """
        self.connection = http.client.HTTPConnection(self.host, self.port)

    def get_headers(self):
        """ Returns the headers need for a auccessful request to blitz.io. """
        private = self.private_key
        headers = {
            "Content-type": "application/json",
            'X-API-User': self.username, 
            'X-API-Key': self.api_key if private is None else private,
            'X-API-Client' : 'python'                
        }
        return headers
    
    def set_private_key(self, key):
        """ Sets the user private key to be used in the request header.  """
        self.private_key = key
    
    def execute(self, post_data):
        """ Sends a queue request to blitz.io RESTful API. """
        path = "/api/1/curl/execute"
        data = json.dumps(post_data)
        self.connection.request("POST", path, data, self.get_headers())
        response = self.connection.getresponse()
        response_string = response.read()
        return json.loads(response_string)
    
    def login(self):
        """ Login to blitz.io RESTful API. """
        path = "/login/api"
        self.connection.request("GET", path, None, self.get_headers())
        response = self.connection.getresponse()
        response_string = response.read()
        return json.loads(response_string)
    
    def job_status(self, job_id):
        """ Sends a job status request to blitz.io  RESTful API. """
        path = "/api/1/jobs/{}/status".format(job_id)
        self.connection.request("GET", path, None, self.get_headers())
        response = self.connection.getresponse()
        response_string = response.read()
        return json.loads(response_string)
    
    def abort_job(self, job_id):
        """ Send a abort request to blitz.io RESTful API. """
        path = "/api/1/jobs/{}/abort".format(job_id)
        self.connection.request("PUT", path, '', self.get_headers())
        response = self.connection.getresponse()
        response_string = response.read()
        return json.loads(response_string)
    
    def close(self):
        """ Closes the connection. """
        self.connection.close()