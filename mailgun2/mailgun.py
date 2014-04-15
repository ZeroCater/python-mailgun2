from __future__ import unicode_literals
import json
import requests

BASE_URL = 'https://api.mailgun.net/v2'


class Mailgun(object):
    def __init__(self, api_key, domain):
        self.auth = ('api', api_key)
        self.base_url = '{0}/{1}'.format(BASE_URL, domain)

    def post(self, path, data, include_domain=True):
        url = self.base_url if include_domain else BASE_URL
        return requests.post(url + path, auth=self.auth, data=data)

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

    def create_list(self, address, name=None, description=None, access_level=None):
        data = {'address': address}
        if name:
            data['name'] = name

        if description:
            data['description'] = description

        if access_level and access_level in ['readonly', 'members', 'everyone']:
            data['access_level'] = access_level

        return self.post('/lists', data, include_domain=False)

    def add_list_member(self, list_name, address, name=None, params=None,
                        subscribed=True, upsert=False):
        data = {'address': address}
        if name:
            data['name'] = name

        if params:
            data['vars'] = json.dumps(params) if isinstance(params, dict) else params

        if not subscribed:
            data['subscribed'] = 'no'

        if upsert:
            data['upsert'] = 'yes'

        return self.post('/lists/%s/members' % list_name, data, include_domain=False)
