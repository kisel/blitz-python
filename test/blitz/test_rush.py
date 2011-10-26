import unittest
import mock
from blitz.rush import Rush
from blitz.api import Error, ValidationError

class  RushTestCase(unittest.TestCase):
    
    def setUp(self):
        self.rush = Rush("user", "public_key", "localhost", 9295, False)

    def test_successful(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"c123"}',
            
            "/api/1/jobs/c123/status": '{"_id":"c123","ok":true,\
            "status":"completed","result":{"region":"california","timeline":[\
            {"duration":1,"total":10,"executed":8,"errors":1,\
            "timeouts":1,"volume":10}, {"duration":2,"total":100,\
            "executed":80,"errors":10,"timeouts":10,"volume":100}]}}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertEqual('california', result.region)
            self.assertIsNotNone(result.timeline)
            self.assertEqual(2, len(result.timeline))
            self.assertEqual(1, result.timeline[0].duration)
            
        options = {'steps':[{'url': 'http://example.com'}],
            'pattern': { 'intervals': [{'start':1, 'end':2}]}}
        self.rush.client.connection = mock.connection(resp)
        self.rush.execute(options, callback)
        
    def test_successful_complex(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"c123"}',
            
            "/api/1/jobs/c123/status": '{"_id":"c123","ok":true,\
            "status":"completed","result":{"region":"california","timeline":[\
            {"duration":1,"total":10,"executed":8,"errors":1,\
            "timeouts":1,"volume":10}, {"duration":2,"total":100,\
            "executed":80,"errors":10,"timeouts":10,"volume":100}]}}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertEqual('california', result.region)
            self.assertIsNotNone(result.timeline)
            self.assertEqual(2, len(result.timeline))
            self.assertEqual(1, result.timeline[0].duration)
            
        options = {'steps':[{'url': 'http://example.com', 'status':200, 
            'cookies': ['cookie1=foo', 'cookie2=bar']}],
            'pattern': { 'intervals': [{'start':1, 'end':2}]}}
        self.rush.client.connection = mock.connection(resp)
        self.rush.execute(options, callback)
        
    def test_fail_login(self):
        resp = {"/login/api":'{"error":"login", "reason":"test"}'}
        
        def callback(result):
            self.assertFalse(True)

        options = {'steps':[{'url': 'http://example.com'}],
            'pattern': { 'intervals': [{'start':1, 'end':2}]}}
        self.rush.client.connection = mock.connection(resp)
        
        with self.assertRaises(Error) as err:
            self.rush.execute(options, callback)
        
        self.assertEqual('login', err.exception.error)
    
    def test_fail_validation_steps(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {}
        self.rush.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.rush.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('steps', err.exception.fields)
        self.assertIn('pattern', err.exception.fields)

    def test_fail_validation_url(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {'steps':[{}]}
        self.rush.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.rush.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('url', err.exception.fields)
        self.assertIn('pattern', err.exception.fields)

    def test_fail_validation_pattern(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {'steps':[{'url': 'http://example.com'}]}
        self.rush.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.rush.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('pattern', err.exception.fields)

    def test_fail_validation_cookie(self):
        resp = {}
        
        def callback(result):
            self.assertFalse(True)

        options = {'steps':[{'cookies':'string'}]}
        self.rush.client.connection = mock.connection(resp)
        
        with self.assertRaises(ValidationError) as err:
            self.rush.execute(options, callback)
        
        self.assertEqual('validation', err.exception.error)
        self.assertIn('url', err.exception.fields)
        self.assertIn('pattern', err.exception.fields)
        self.assertIn('cookies', err.exception.fields)


    def test_fail_queue(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"error":"throttle", \
            "reason":"Slow down please!"}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertTrue('error' in result)
            self.assertEqual('throttle', result['error'])
        
        options = {'steps':[{'url': 'http://example.com'}],
            'pattern': { 'intervals': [{'start':1, 'end':2}]}}
        self.rush.client.connection = mock.connection(resp)
        with self.assertRaises(Error) as err:
            self.rush.execute(options, callback)
        

if __name__ == '__main__':
    unittest.main()