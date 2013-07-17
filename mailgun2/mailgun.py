from __future__ import unicode_literals
import requests


BASE_URL = 'https://api.mailgun.net/v2'
class Mailgun(object):
    def __init__(self, api_key, domain):
        self.auth = ('api', api_key)
        self.base_url = '{0}/{1}'.format(BASE_URL, domain)

    def post(self, path, data):
        return requests.post(self.base_url + path, auth=self.auth, data=data)

    def send_message(self, from_email, to, cc=None, bcc=None,
                     subject=None, text=None, html=None, tags=None):
        # sanity checks
        assert (text or html)

        data = {
            'from': from_email,
            'to': to,
            'cc': cc or [],
            'bcc': bcc or [],
            'subject': subject or '',
            'text': text or '',
            'html': html or '',
        }

        return self.post('/messages', data)
