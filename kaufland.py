import requests
from requests.adapters import Retry
from requests.adapters import HTTPAdapter
import logging
import time

# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s %(message)s',
# )

LOG = logging.getLogger(__name__)

class HTTPConnection:
    def __init__(self) -> None:
        self.session = requests.session()
        self.erros = 0
        self.backoff_factor = 30

    def request(self, method, url, headers=None, params=None, data=None, retries=0, **kwargs):
        attempt = 1
        while True:
            resp = self.session.request(method=method, url=url, headers=headers, params=params, data=data, **kwargs)

            if not retries or attempt > retries:
                return resp

            if resp.status_code in [413, 429, 503]:
                LOG.info(f'status code: {resp.status_code} - retrying.')
                LOG.info(f'resp content: {resp.text}.')
                attempt += 1
                time.sleep(self.backoff_time(attempt))
            else:
                return resp

    def backoff_time(self, attempt):
        return self.backoff_factor * (2 ** (attempt))