import requests_cache
import const as c
import sys
session = requests_cache.CachedSession('demo_cache')

from log_setup import *

def make_request(params, header):
	req = session.get(c.url, params=params, headers=header)
	if req.status_code != 200:
		logging.debug(f"Status of request is {req.status_code}. Aborting...")
		sys.exit()
	return req
