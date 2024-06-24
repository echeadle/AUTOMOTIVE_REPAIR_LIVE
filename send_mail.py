import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

send_email_declaration = {
    "name": "send_mail",
    "description": "Sends an email using SMTP with a specified subject, body and recipient.",
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "The subject of the email"
            },
            "body": {
                "type": "string",
                "description": "The body of the email"
            },
            "to_email": {
                "type": "string",
                "description": "The recipient of the email"
            },
        },
        "required": ["subject", "body", "to_email"]
    },
}

def send_mail(subject, body, to_email):
    sender = "Private Person <from@example.com>"
    
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to_email
    
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("0182053cc23f0e", smtp_password)
        server.send_message(message)
        return "Email has been sent"

if __name__ == "__main__":
    send_mail("Testmail", "Dear Mr. X", "bob@foe.de")