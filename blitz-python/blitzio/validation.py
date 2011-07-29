__author__="ghermeto"
__date__ ="$28/07/2011 19:13:12$"

import re
from urllib.parse import urlparse

def validate_url(url):
    parsed = urlparse(url)
    return parsed.scheme and parsed.netloc

def validate_int(value):
    str_value = str(value)
    return True if re.search("^[0-9]+$", str_value) else False

def validate_list(lst):
    return isinstance(lst, types.ListType) or isinstance(lst, types.TupleType)

def validate(options):
    failed = []
    if options.has_key('referrer') and not validate_url(options['referrer']):
        failed.append('referrer')
    if options.has_key('status') and not validate_int(options['status']):
        failed.append('status')
    if options.has_key('timeout') and not validate_int(options['timeout']):
        failed.append('timeout')
    if options.has_key('cookies') and not validate_list(options['cookies']):
        failed.append('cookies')
    if options.has_key('headers') and not validate_list(options['headers']):
        failed.append('headers')
    return failed
        