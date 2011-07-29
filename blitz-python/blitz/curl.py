__author__="ghermeto"
__date__ ="$28/07/2011 18:02:56$"

import time
from blitz.api import Client

class ValidationError(blitz.api.Error):
    """ Validation error for Blitz api. """
    
    def __init__(self, reason, fields = []):
        self.error = "validation"
        self.reason = reason
        self.fields = fields

class Base:
    """ Base class used by Blitz curl tests. """
    
    def __init__(self, user, api_key, host=None, port=None, connect=True):
        self.client = Client(user, api_key, host, port, connect)
        self.job_id = None
    
    def execute(self, options, callback):
        """ Execute the test and waits for job_status notifications from the
            server. """
        self._validate(options) # raises error if options isn't valid
        self._check_authentication() #authenticates
        queue_response = self.client.execute(options)
        if queue_response is None: # raise error if we get no response
            raise Error('client', 'No response') 
        elif queue_response.has_key('error'): # callback with error message
            callback(queue_response)
            return
        self.job_id = queue_response['job_id']
        self.job_status(callback)
    
    def job_status(self, callback):
        """ """
        if self.job_id is None:
            raise Error('client', 'No job')
        self._check_authentication() #authenticates
        status = None
        while status != 'completed':
            time.sleep(2)
            job = self.client.job_status(self.job_id)
            if job is None:
                raise Error('client', 'No response') 
            elif job.has_key('error'):
                callback(job)
                break
            elif job.has_key('result') and job['result'].has_key('error'):
                callback(job['result'])
                continue
            elif job['status'] == 'queued' \
            or (job['status'] == 'running' and not job.has_key('result')):
                continue
            result = self._format_result(job['result'])
            callback(result)
            status = job['status']
    
    def _validate(self, options):
        """ Method should be overriden by subclasses and raise a ValidationError
            if validation fails. """
        pass
    
    def _format_result(self, result):
        """ Method should be overriden by subclasses and return the appropritate
            result object to be passed to the callback. """
        pass
    
    def _check_authentication(self):
        """ Authenticates the Client if necesary, storing the private key. """
        if self.client.private_key is None: 
            response = self.client.login()
            if response is None:
                raise Error('client', 'No response') 
            elif response.has_key('error'):
                raise Error(response['error'], response['reason'])
            else:
                self.client.set_private_key(response['api_key'])
    
    def abort(self):
        """ Aborts the current job. """
        try:
            self.client.abort_job(self.job_id)
        except:
            pass