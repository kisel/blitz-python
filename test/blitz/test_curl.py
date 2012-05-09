import unittest
import mock
import blitz.sprint
import blitz.rush
from blitz.api import Error
from blitz.curl import Test

class  CurlTestCase(unittest.TestCase):
    
    def setUp(self):
        self.test = Test("user", "public_key", "localhost", 9295, False)

    def test_successful_sprint(self):
        resp = {"/api/1/parse": '{"ok":true,\
            "command":{"steps":[{"url":"http://example.com"}]}}',
            
            "/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"a123"}',
            
            "/api/1/jobs/a123/status": '{"_id":"a123","ok":true,\
            "status":"completed","result":{"region":"california","duration":10,\
            "steps":[{"connect":1,"request":{"line":"GET / HTTP/1.1",\
            "method":"GET","url":"http://localhost:9295","headers":{},\
            "content":"MTIzNA=="},"duration":10,\
            "response":{"line":"GET / HTTP/1.1","message":"message",\
            "status":200,"headers":{},"content":"MTIzNA=="}}]}}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertIs(result.__class__, blitz.sprint.Result)
            self.assertEqual('california', result.region)
            self.assertEqual(10, result.duration)
            self.assertEqual(10, result.steps[0].duration)
            self.assertIsNotNone(result.steps[0].request)
            self.assertIsNotNone(result.steps[0].response)
            self.assertEqual('GET', result.steps[0].request.method)
            self.assertEqual(200, result.steps[0].response.status)
            self.assertEqual('1234', result.steps[0].request.content)
            
        options = {"command": "http://example.com"}
        self.test.client.connection = mock.connection(resp)
        self.test.parse(options, callback)

    def test_successful_rush(self):
        resp = {"/api/1/parse": '{"ok":true,\
            "command":{"steps":[{"url":"http://example.com"}],\
            "pattern":{"iterations":1,"intervals":\
            [{"iterations":1,"start":5,"end":10,"duration":10}]}}}',
            
            "/login/api":'{"ok":true, "api_key":"private-key"}',
        
            "/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"c123"}',
            
            "/api/1/jobs/c123/status": '{"_id":"c123","ok":true,\
            "status":"completed","result":{"region":"california","timeline":[\
            {"duration":1,"total":10,"executed":8,"errors":1,\
            "timeouts":1,"volume":10}, {"duration":2,"total":100,\
            "executed":80,"errors":10,"timeouts":10,"volume":100}]}}'}
            
        def callback(result):
            self.assertIsNotNone(result)
            self.assertIs(result.__class__, blitz.rush.Result)
            self.assertEqual('california', result.region)
            self.assertIsNotNone(result.timeline)
            self.assertEqual(2, len(result.timeline))
            self.assertEqual(1, result.timeline[0].duration)
            
        options = {"-p 5-10:10 command": "http://example.com"}
        self.test.client.connection = mock.connection(resp)
        self.test.parse(options, callback)
        
        
    def test_fail_parse(self):
        resp = {"/api/1/parse":'{"error":"test", "reason":"testing error"}',
        
            "/login/api":'{"ok":true, "api_key":"private-key"}'}
        
        def callback(result):
            self.assertFalse(True)

        options = {"abc": "--ppp http://example.com"}
        self.test.client.connection = mock.connection(resp)
        
        with self.assertRaises(Error) as err:
            self.test.parse(options, callback)
        
        self.assertEqual('test', err.exception.error)

if __name__ == '__main__':
    unittest.main()