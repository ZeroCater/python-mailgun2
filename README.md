python-mailgun-v2
=================

A super simple API for interacting with mailgun. Currently only supports
sending messages. Powered by
[Requests](http://docs.python-requests.org/en/latest/)

Python 3 support should be there but is currently untested.

Usage:

    from mailgun2 import Mailgun
    mailer = Mailgun('apikey', 'mailgun domain')
    mailer.send_message('from@mailgun.com', ['to@you.com',
'others@you.com'], subject='Hi!', text='Sweet.')

Optional arguments:

    subject: string subject of the email
    text: string body of the email. Either text or html is required.
    html: string HTML of the email. Either text or html is required.
    cc: list of cc addresses.
    bcc: list of bcc addresses.
    tags: list of mailgun tags to associate with the email.

Pull requests welcome!
