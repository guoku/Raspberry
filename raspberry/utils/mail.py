# coding=utf-8
from django.core import mail

class Mail(object):
    
    def __init__(self, subject, message, content_type = 'html'):
        self.subject = subject
        self.message = message 
    
    def send(self, address):
        _conn = mail.get_connection()
        _conn.open()
        _email = mail.EmailMessage(self.subject, self.message, u'果库<noreply@post.guoku.com>', [address])
        _email.content_subtype = "html"
        _email.send()
        _conn.close()
