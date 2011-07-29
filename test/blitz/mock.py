__author__="ghermeto"
__date__ ="$28/07/2011 12:33:25$"

def connection(responses={}):
    return MockHTTPConnection(responses)

class MockHTTPConnection:
    """ Mock HTTP connection. Receives a hash with the paths and expected 
        response strings for each path and returns a mock response with the
        appropriated response for the path requested. """
    
    def __init__(self, responses={}):
        self.responses = responses
    
    def request(self, method, path, body=None, headers={}):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers
    
    def getresponse(self):
        response = self.responses[self.path]
        return MockHTTPResponse(response)
    
    def close(self):
        pass

class MockHTTPResponse:
    """ Mock response object. Returns the response on read. """
    
    def __init__(self, response=''):
        self.response = response
    
    def read(self, amt=0):
        return self.response