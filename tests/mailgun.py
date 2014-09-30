import unittest

from mock import patch, MagicMock

import mailgun2

class MailgunTestBase(unittest.TestCase):
    def setUp(self):
        self.api_key = 'test_api_key'
        self.domain = 'test_domain'
        self.mailgun = mailgun2.Mailgun(self.api_key, self.domain)
        self.requests_patcher = patch('mailgun2.mailgun.requests')
        self.mock_requests = self.requests_patcher.start()

    def tearDown(self):
        self.requests_patcher.stop()


class SendMessageTest(MailgunTestBase):
    def test_send_simple_message(self):
        pass

    def test_require_text_or_html(self):
        pass

    def test_reply_to(self):
        pass

    def test_headers(self):
        pass

    def test_inlines_attachments(self):
        pass


class CreateListTest(MailgunTestBase):
    pass
    # TODO


class AddListTest(MailgunTestBase):
    pass
    # TODO