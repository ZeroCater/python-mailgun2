from __future__ import unicode_literals
import json
import requests

BASE_URL = 'https://api.mailgun.net/v2'


class Mailgun(object):
    def __init__(self, api_key, domain):
        self.auth = ('api', api_key)
        self.base_url = '{0}/{1}'.format(BASE_URL, domain)

    def post(self, path, data, files=None, include_domain=True):
        url = self.base_url if include_domain else BASE_URL
        return requests.post(url + path, auth=self.auth, data=data, files=files)

    def send_message(self, from_email, to, cc=None, bcc=None,
                     subject=None, text=None, html=None, tags=None,
                     reply_to=None, headers=None, inlines=None, attachments=None, campaign_id=None):
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

        if reply_to:
            data['h:Reply-To'] = reply_to
        if headers:
            for k, v in headers.items():
                data["h:%s" % k] = v
        if campaign_id:
            data['o:campaign'] = campaign_id
        files = []
        if inlines:
            for filename in inlines:
                files.append(('inline', open(filename)))
        if attachments:
            for filename, content_type, content in attachments:
                files.append(('attachment', (filename, content, content_type)))

        return self.post('/messages', data, files=files)

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
