from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


class Email:
    def __init__(self, host, user, password, name=None):
        self.host = host
        self.user = user
        self.password = password
        self.name = name or self.user

    def connect(self):
        smtp = SMTP(self.host)
        smtp.starttls()
        smtp.login(self.user, self.password)

        return smtp

    def send(self, to, subject, text, html=None):
        smtp = self.connect()

        if html:
            message = MIMEMultipart('alternative')
            message.attach(MIMEText(text, 'plain'))
            message.attach(MIMEText(html, 'html'))
        else:
            message = MIMEText(text, 'plain')

        message['subject'] = subject
        message['to'] = to
        message['from'] = f'{self.name} <{self.user}>'

        smtp.send_message(message)
        smtp.close()


    def send_verification(self, user, url):
        text = """\
            Hi, {name}.

            Please verify your email address by navigating to the URL below:

            {url}

            Thank you.
            """.format(name=user.name, url=url)

        html = """\
            <html>
                <head></head>
                <body>
                    <p>Hi, {name}.</p>
                    <p>
                        Please verify your email address by clicking on the
                        link below:
                    </p>
                    <p><a href="{url}">Verify</a></p>
                    <p>Thank you.</p>
                </body>
            </html>
            """.format(name=user.name, url=url)

        self.send(user.email, "Verify Your Email", text, html)


    def send_password(self, user, password):
        text = """\
            Hi, {name}.

            At your request, your password has been reset:

            Username: {id}
            Password: {password}

            Thank you.
            """.format(name=user.name, id=user.id, password=password)

        html = """\
            <html>
                <head></head>
                <body>
                    <p>Hi, {name}.</p>
                    <p>
                        At your request, your password has been reset:
                    </p>
                    <p>
                        <strong>Username:</strong> {id}<br/>
                        <strong>Password:</strong>
                        <span style="font-family: monospace">{password}</span>
                    </p>
                    <p>Thank you.</p>
                </body>
            </html>
            """.format(name=user.name, id=user.id, password=password)

        self.send(user.email, "Password Reset", text, html)

