import smtplib
from urllib.parse import urlencode
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from app.core.config import settings


def send_email(email_to: str, subject_template: str, html_template: str):
    try:
        email_smtp_login = settings.smtp_login
        email_smtp_password = settings.smtp_password
        message = MIMEMultipart()
        message["From"] = formataddr(("Workdirect", settings.smtp_from))
        message["To"] = str(email_to)
        message["Subject"] = str(subject_template)
        message.attach(MIMEText(html_template, "html"))
        server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        server.login(email_smtp_login, email_smtp_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception:
        return False


def send_reset_password_email(email_to: str, token: str) -> bool:
    subject_template = "Workdirect: Восстановление пароля"
    query_string = str(urlencode(OrderedDict(token=token)))
    url = str(settings.FRONT_DOMAIN + "/reset_password?" + query_string)
    html_template = """
                <html>
                    <body>
                        <p>
                            Здравствуйте!
                            <br>
                            <br>
                            Вы отправили запрос на восстановление пароля от почтового ящика.
                            <br>
                            <br>
                            Для изменения пароля нажмите на ссылку ниже:
                            <br>
                            <br>
                            <a href={url}>Восстановить пароль</a>
                            <br>
                            <br>
                            С уважением Workdirect.
                        </p>
                    </body>
                </html>
                """.format(url=url)
    return send_email(email_to=email_to, subject_template=subject_template, html_template=html_template)
