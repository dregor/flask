from flask.ext.mail import Message
from flask import render_template, flash
from helpers import async
from app import mail, app
from config import INFO_EMAIL


@async
def send_async_email(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    # send_async_email(msg)


def send_mail_register(user):
	app.logger.info('send register mail to' + str(user))
	return send_email("Hello to you %s from Flask-site!" % user.nickname, INFO_EMAIL, [user.email], render_template("email_register.txt", user=user, INFO_EMAIL=INFO_EMAIL), render_template("email_register.txt", user=user, INFO_EMAIL=INFO_EMAIL))