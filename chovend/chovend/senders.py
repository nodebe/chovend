import os
from dotenv import load_dotenv
from django.core.mail import send_mail, BadHeaderError
from chovend.errors import ServerError
from .errors import UserError

load_dotenv()

def send_email(subject, recipient:str, message):
    try:
        send_mail(
            subject = subject,
            recipient_list = [recipient],
            message = '',
            from_email = os.environ.get('DEFAULT_FROM_EMAIL'),
            html_message=message
        )

        return True
    except BadHeaderError:
        raise UserError('Invalid Header found!')
    
    except Exception as e:
        raise ServerError(e, 'Email not sent, try again!')