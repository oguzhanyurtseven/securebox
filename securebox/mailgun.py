__author__ = 'cemkiy'

import requests
class mailgun:
    def __init__(self):
        self.key = 'your mailgun key---'
        self.sandbox = 'your mailgun key----'

    def send_mail(self, from_email, email_to, title, text):
        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox)
        request = requests.post(request_url, auth=('api', self.key), data={
        'from': from_email,
        'to': email_to,
        'subject': title,
        'text': text
        })
        output = 'Status: {0}'.format(request.status_code) + 'Body: {0}'.format(request.text)
        print output

    def send_mail_with_html(self, email_to, html):
        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox)
        request = requests.post(request_url, auth=('api', self.key), data={
        'from': self.recipient,
        'to': email_to,
        'subject': 'Hello',
        'html': html
        })
        output = 'Status: {0}'.format(request.status_code) + 'Body: {0}'.format(request.text)
        print output




    # template = get_template("mail_activation.html")
    # context = Context({'username': 'cem'})
    # content = template.render(context)
    # mailgun_operator = mailgun()
    # mailgun_operator.send_mail_with_html(member_user_auth.email, content)
