import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def enviar_email(email, subject, body):
    
    sg = sendgrid.SendGridAPIClient(os.getenv('SEND_GRID_CLIENT_KEY'))
    from_email = Email("noreply@arcadearena.com")
    to_email = To(email)
    subject = subject
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)
    
    mail_json = mail.get()
    
    response = sg.client.mail.send.post(request_body=mail_json)
    return response

