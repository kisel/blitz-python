import unittest
import mock
from blitz.sprint import Sprint
from blitz.api import Error, ValidationError

class  SprintTestCase(unittest.TestCase):
    
    def setUp(self):
        self.sprint = Sprint("user", "public_key", "localhost", 9295, False)

    def test_successful(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"a123"}',
            
            "/api/1/jobs/a123/status": '{"_id":"a123","ok":true,\
            "status":"completed","result":{"region":"california","duration":10,\
            "connect":1,"request":{"line":"GET / HTTP/1.1","method":"GET",\
            "url":"http://localhost:9295","headers":{},\
            "content":"MTIzNA=="},\
            "response":{"line":"GET / HTTP/1.1","message":"message",\
            "status":200,"headers":{},"content":"MTIzNA=="}}}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertEqual('california', result.region)
            self.assertEqual(10, result.duration)
            self.assertIsNotNone(result.request)
            self.assertIsNotNone(result.response)
            self.assertEqual('GET', result.request.method)
            self.assertEqual(200, result.response.status)
            self.assertEqual('1234', result.request.content)
            
        options = {'url': 'http://example.com'}
        self.sprint.client.connection = mock.connection(resp)
        self.sprint.execute(options, callback)
        
    def test_fail_login(self):
        resp = {"/login/api":'{"error":"login", "reason":"test"}'}
        
        def callback(result):
            self.assertFalse(True)

        options = {'url': 'http://example.com'}
        self.sprint.client.connection = mock.connection(resp)
        
        with self.assertRaises(Error) as err:
            self.sprint.execute(options, callback)
        
        self.assertEqual('login', err.exception.error)
    
    def test_fail_validation(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {}
        self.sprint.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.sprint.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('url', err.exception.fields)

    def test_fail_validation_cookie(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {'cookies':'string'}
        self.sprint.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.sprint.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('url', err.exception.fields)
        self.assertIn('cookies', err.exception.fields)


    def test_fail_queue(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"error":"throttle", \
            "reason":"Slow down please!"}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertTrue('error' in result)
            self.assertEqual('throttle', result['error'])
            
        options = {'url': 'http://example.com'}
        self.sprint.client.connection = mock.connection(resp)
        self.sprint.execute(options, callback)
        

if __name__ == '__main__':
    unittest.main()