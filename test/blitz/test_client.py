import unittest
import mock
from blitz.api import Client

class  ClientTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("user", "public_key", "localhost", 9295, False)

    def tearDown(self):
        self.client.close()

    def test_successful_login(self):
        resp = {"/login/api":'{"ok":true, "api_key":"private-key"}'}
        self.client.connection = mock.connection(resp)
        response = self.client.login()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['ok'])
        self.assertTrue(response['ok'])
        self.assertEqual('private-key', response['api_key'])
    
    def test_failed_login(self):
        resp = {"/login/api":'{"error":"login", "reason":"test"}'}
        self.client.connection = mock.connection(resp)
        response = self.client.login()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['error'])
        self.assertEqual('login', response['error'])
        self.assertEqual('test', response['reason'])
        
    def test_successful_execute(self):
        resp = {"/api/1/curl/execute":'{"ok":true, "status":"queued", \
            "region":"california", "job_id":"a123"}'}
        self.client.connection = mock.connection(resp)
        data = {'steps': [{'url':'http://example.com'}] }
        response = self.client.execute(data)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['ok'])
        self.assertTrue(response['ok'])
        self.assertEqual('a123', response['job_id'])
        self.assertEqual('california', response['region'])
        self.assertEqual('queued', response['status'])
        body = self.client.connection.body
        self.assertEqual('{"steps": [{"url": "http://example.com"}]}', body)
    
    def test_job_status(self):
        resp = {"/api/1/jobs/c123/status":'{"_id":"c123", "ok":true,\
            "result":{"region":"california","timeline":[\
            {"duration":1,"total":10,"executed":8,"errors":1,\
            "timeouts":1,"volume":10}, {"duration":2,"total":100,\
            "executed":80,"errors":10,"timeouts":10,"volume":100}]}}'}
        self.client.connection = mock.connection(resp)
        response = self.client.job_status('c123')
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['ok'])
        self.assertTrue(response['ok'])
        self.assertEqual('c123', response['_id'])

    def test_abort_job(self):
        resp = {"/api/1/jobs/c123/abort":'{"ok":true}'}
        self.client.connection = mock.connection(resp)
        response = self.client.abort_job('c123')
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['ok'])
        self.assertTrue(response['ok'])
        path = self.client.connection.path
        self.assertEqual('/api/1/jobs/c123/abort', path)

if __name__ == '__main__':
    unittest.main()

