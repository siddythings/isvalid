import re
from urllib.parse import urlparse
import traceback
import os
from flask_mail import Mail, Message

# If any other HTTP method is used, return a 405 Method Not Allowed


def method_not_allowed():
    return {'message': 'Method not allowed'}, 405

# Function to send an error email


def send_error_email(mail, error):
    subject = "Flask App Error Alert"
    sender = os.getenv('MAIL_USERNAME')
    recipients = os.getenv('MAIL_USERNAME', "").split(
        ",")  # Add any recipients here

    # Capture error trace
    error_trace = traceback.format_exc()

    # Create the email body
    body = f"An error occurred in the Flask app:\n\n{error_trace}"

    # Send the email
    msg = Message(subject, sender=sender, recipients=recipients, body=body)
    mail.send(msg)


def validate_url(url: str) -> str:
    # Regular expression for validating a URL
    url_pattern = re.compile(
        r'^(https?://)?'           # Optional scheme (http or https)
        r'((www\.)?[^/]+)'         # Hostname (optional www)
        r'(\.[a-z]{2,})'           # Domain extension
        r'(/[^\s]*)?'              # Optional path
        r'(\?[^\s]*)?$'            # Optional query string
    )

    if url_pattern.match(url):
        parsed_url = urlparse(url)

        # Ensure URL has a scheme and netloc
        if parsed_url.scheme and parsed_url.netloc:
            return url  # URL is valid as it has a scheme and a valid netloc

        # If scheme is missing, assume "http"
        return f"https://{url}"

    return "Invalid URL"
