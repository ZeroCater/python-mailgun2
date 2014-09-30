import os
import unittest

from mock import patch, MagicMock

import mailgun2

class MailgunTestBase(unittest.TestCase):
    def setUp(self):
        self.api_key = 'test_api_key'
        self.domain = 'test.domain'
        self.mailgun = mailgun2.Mailgun(self.api_key, self.domain)
        self.post_patcher = patch('mailgun2.mailgun.requests.post')
        self.mock_post = self.post_patcher.start()

    def tearDown(self):
        self.post_patcher.stop()


class SendMessageTest(MailgunTestBase):
    def test_send_simple_message(self):
        self.mailgun.send_message(
            'from@example.com',
            'to@example.com',
            cc='cc@example.com',
            bcc='bcc@example.com',
            subject='Test subject',
            text='Test text',
            html='Test html'
        )
        self.assertTrue(self.mock_post.called)
        url = self.mock_post.call_args[0][0]
        auth = self.mock_post.call_args[1]['auth']
        data = self.mock_post.call_args[1]['data']
        files = self.mock_post.call_args[1]['files']
        self.assertEqual(url, 'https://api.mailgun.net/v2/test.domain/messages')
        self.assertEqual(auth, ('api', 'test_api_key'))
        self.assertEqual(files, [])
        self.assertEqual(data['from'], 'from@example.com')
        self.assertEqual(data['to'], 'to@example.com')
        self.assertEqual(data['cc'], 'cc@example.com')
        self.assertEqual(data['bcc'], 'bcc@example.com')
        self.assertEqual(data['subject'], 'Test subject')
        self.assertEqual(data['text'], 'Test text')
        self.assertEqual(data['html'], 'Test html')

    def test_defaults(self):
        self.mailgun.send_message(
            'from@example.com',
            'to@example.com',
            html='Test html'
        )
        data = self.mock_post.call_args[1]['data']
        self.assertEqual(data['cc'], [])
        self.assertEqual(data['bcc'], [])
        self.assertEqual(data['subject'], '')
        self.assertEqual(data['text'], '')

    def test_require_text_or_html(self):
        with self.assertRaises(AssertionError):
            self.mailgun.send_message(
                'from@example.com',
                'to@example.com'
            )

    def test_reply_to(self):
        self.mailgun.send_message(
            'from@example.com',
            'to@example.com',
            html='Test html',
            reply_to='reply@example.com',
        )
        data = self.mock_post.call_args[1]['data']
        self.assertEqual(data['h:Reply-To'], 'reply@example.com')

    def test_headers(self):
        self.mailgun.send_message(
            'from@example.com',
            'to@example.com',
            html='Test html',
            headers={'header':'value'}
        )
        data = self.mock_post.call_args[1]['data']
        self.assertEqual(data['h:header'], 'value')

    def test_inlines_attachments(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        license_file = current_path+'/../LICENSE'
        self.mailgun.send_message(
            'from@example.com',
            'to@example.com',
            html='Test html',
            inlines=[license_file],
            attachments=[('license', 'text', open(license_file,'r'))]
        )
        files = self.mock_post.call_args[1]['files']
        self.assertEqual(files[0][0], 'inline')
        self.assertEqual(files[0][1].name, license_file)
        self.assertEqual(files[1][0], 'attachment')
        self.assertEqual(files[1][1][0], 'license')
        self.assertEqual(files[1][1][1].name, license_file)
        self.assertEqual(files[1][1][2], 'text')


class CreateListTest(MailgunTestBase):
    pass
    # TODO


class AddListTest(MailgunTestBase):
    pass
    # TODO