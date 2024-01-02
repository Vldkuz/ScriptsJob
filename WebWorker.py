import urllib.request
from http import HTTPStatus
from urllib.error import HTTPError, URLError

std_url = 'https://docs.ideco.dev'
std_header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/99.0.4844.84 Safari/537.36",
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}


class WebWorker:
    def __init__(self, url=std_url):
        if WebWorker.check_ref(url):
            self.url_check = url
        else:
            raise Exception("Invalid URL")

    def check_alias(self, alias):
        check_alias = f'{self.url_check}/{alias}'
        return WebWorker.check_ref(check_alias) or WebWorker.check_ref_forbidden(check_alias)

    @staticmethod
    def check_ref(ref):
        try:
            req = urllib.request.Request(ref, headers=std_header)
            check = urllib.request.urlopen(req)
            return check.getcode() == HTTPStatus.OK
        except (HTTPError, URLError):
            return False

    @staticmethod
    def check_ref_forbidden(ref):
        try:
            req = urllib.request.Request(ref, headers=std_header)
            check = urllib.request.urlopen(req)
            return check.getcode() == HTTPStatus.FORBIDDEN
        except (HTTPError, URLError):
            return False
