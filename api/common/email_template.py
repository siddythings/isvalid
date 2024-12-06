import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

ses_client = boto3.client(
    "ses",
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_SES_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SES_SECRET_ACCESS_KEY"),
)


class Email:
    @staticmethod
    def send_email(email, html_template, TextPart, SubjectPart):
        try:
            response = ses_client.send_email(
                Source="order@lucir.io",
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": SubjectPart, "Charset": "UTF-8"},
                    "Body": {
                        "Text": {
                            "Data": TextPart,
                            "Charset": "UTF-8",
                        },
                        "Html": {
                            "Data": html_template,
                            "Charset": "UTF-8",
                        },
                    },
                },
            )
            print("Email sent! Message ID:", response["MessageId"])
        except (NoCredentialsError, PartialCredentialsError) as e:
            print("Credentials error:", e)
        except Exception as e:
            print("Error sending email:", e)


class EamilTemplates:
    @staticmethod
    def digital_download(name, download_link, order_id):
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Digital Download Product</title>
            <style>
                body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                }
                .container {
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                color: #333333;
                text-align: center;
                }
                .content {
                font-size: 16px;
                color: #666666;
                line-height: 1.5;
                margin: 20px 0;
                }
                .btn {
                display: inline-block;
                padding: 12px 24px;
                color: #ffffff;
                background-color: #007BFF;
                text-decoration: none;
                border-radius: 4px;
                text-align: center;
                font-size: 16px;
                margin: 20px auto;
                display: block;
                max-width: 200px;
                }
                .btn:hover {
                background-color: #0056b3;
                }
                .footer {
                font-size: 12px;
                color: #999999;
                text-align: center;
                margin-top: 30px;
                }
                .footer a {
                color: #007BFF;
                text-decoration: none;
                }
                .footer a:hover {
                text-decoration: underline;
                }
            </style>
            </head>
            <body>
            <div class="container">
                <h1>Thank You for Your Purchase!</h1>
                <p class="content">
                Hi {{name}},<br><br>
                Thank you for purchasing our digital product! We're excited for you to get started.
                </p>
                <b>Order ID: {{order_id}}</b>
                <p class="content">
                Click the button below to download your product:
                </p>
                <a href="{{download_link}}" class="btn">Download Now</a>
                <p class="content">
                If you have any questions or need further assistance, feel free to reply to this email or reach out to our support team.
                </p>
                <p class="content">Enjoy your new download!</p>
                <div class="footer">
                <p>&copy; lucir.io | <a href="https://lucir.io">Visit our website</a></p>
                <p><a href="[Unsubscribe Link]">Unsubscribe</a></p>
                </div>
            </div>
            </body>
            </html>
            """
        html_content = (
            html_template.replace("{{name}}", name)
            .replace("{{download_link}}", download_link)
            .replace("{{order_id}}", order_id)
        )
        SubjectPart = "Thank you for purchasing our digital product!"
        TextPart = (
            "Thank you for your purchase! Click the link to download your product."
        )
        return html_content, SubjectPart, TextPart

    @staticmethod
    def session_booking(
        name, session_name, session_date, session_time, booking_link, order_id
    ):
        html_template = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Session Booking Confirmation</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        color: #333333;
                        text-align: center;
                    }
                    .content {
                        font-size: 16px;
                        color: #666666;
                        line-height: 1.5;
                        margin: 20px 0;
                    }
                    .btn {
                        display: inline-block;
                        padding: 12px 24px;
                        color: #ffffff;
                        background-color: #007BFF;
                        text-decoration: none;
                        border-radius: 4px;
                        text-align: center;
                        font-size: 16px;
                        margin: 20px auto;
                        display: block;
                        max-width: 200px;
                    }
                    .btn:hover {
                        background-color: #0056b3;
                    }
                    .footer {
                        font-size: 12px;
                        color: #999999;
                        text-align: center;
                        margin-top: 30px;
                    }
                    .footer a {
                        color: #007BFF;
                        text-decoration: none;
                    }
                    .footer a:hover {
                        text-decoration: underline;
                    }
                </style>
                </head>
                <body>
                <div class="container">
                    <h1>Session Booking Confirmed</h1>
                    <p class="content">
                        Hi {{name}},<br><br>
                        Thank you for booking a session with us! Here are the details of your session:
                    </p>
                    <p class="content">
                        <strong>Order ID:</strong> {{order_id}}<br>
                        <strong>Session:</strong> {{session_name}}<br>
                        <strong>Date:</strong> {{session_date}}<br>
                        <strong>Time:</strong> {{session_time}}<br>
                    </p>
                    <p class="content">
                        To manage your booking or reschedule, click the button below:
                    </p>
                    <a href="{{manage_booking_link}}" class="btn">Manage Booking</a>
                    <p class="content">
                        If you have any questions or need further assistance, feel free to reach out to us.
                    </p>
                    <div class="footer">
                        <p>&copy; lucir.io | <a href="https://lucir.io">Visit our website</a></p>
                        # <p><a href="[Unsubscribe Link]">Unsubscribe</a></p>
                    </div>
                </div>
                </body>
                </html>
        """
        html_content = (
            html_template.replace("{{name}}", name)
            .replace("{{session_name}}", session_name)
            .replace("{{session_date}}", session_date)
            .replace(
                "{{session_time}}",
                str(session_time.get("start") + "-" + session_time.get("end")),
            )
            .replace("{{booking_link}}", booking_link)
            .replace("{{order_id}}", order_id)
        )
        SubjectPart = "Your Session Booking is Confirmed!!"
        TextPart = "Thank you for booking a session with us!"
        return html_content, SubjectPart, TextPart

    @staticmethod
    def webinar(name, webinar_title, webinar_date, webinar_time, join_link):
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Webinar Registration Confirmation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333333;
                    text-align: center;
                }
                .content {
                    font-size: 16px;
                    color: #666666;
                    line-height: 1.5;
                    margin: 20px 0;
                }
                .btn {
                    display: inline-block;
                    padding: 12px 24px;
                    color: #ffffff;
                    background-color: #28a745;
                    text-decoration: none;
                    border-radius: 4px;
                    text-align: center;
                    font-size: 16px;
                    margin: 20px auto;
                    display: block;
                    max-width: 200px;
                }
                .btn:hover {
                    background-color: #218838;
                }
                .footer {
                    font-size: 12px;
                    color: #999999;
                    text-align: center;
                    margin-top: 30px;
                }
                .footer a {
                    color: #007BFF;
                    text-decoration: none;
                }
                .footer a:hover {
                    text-decoration: underline;
                }
            </style>
            </head>
            <body>
            <div class="container">
                <h1>You're Registered for the Webinar!</h1>
                <p class="content">
                    Hi {{name}},<br><br>
                    Thank you for registering for our upcoming webinar! Here are the details:
                </p>
                <p class="content">
                    <strong>Webinar:</strong> {{webinar_title}}<br>
                    <strong>Date:</strong> {{webinar_date}}<br>
                    <strong>Time:</strong> {{webinar_time}}<br>
                </p>
                <p class="content">
                    Click the button below to join the webinar at the scheduled time:
                </p>
                <a href="{{join_link}}" class="btn">Join Webinar</a>
                <p class="content">
                    If you have any questions or need assistance, please feel free to reach out.
                </p>
                <div class="footer">
                    <p>&copy; Your Company | <a href="https://yourcompany.com">Visit our website</a></p>
                    <p><a href="[Unsubscribe Link]">Unsubscribe</a></p>
                </div>
            </div>
            </body>
            </html>
        """
        html_content = (
            html_template.replace("{{name}}", name)
            .replace("{{webinar_title}}", webinar_title)
            .replace("{{webinar_date}}", webinar_date)
            .replace("{{webinar_time}}", webinar_time)
            .replace("{{join_link}}", join_link)
        )
        return html_content

    @staticmethod
    def e_course(name, course_name, username, password, course_access_link):
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>E-Course Registration Confirmation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333333;
                    text-align: center;
                }
                .content {
                    font-size: 16px;
                    color: #666666;
                    line-height: 1.5;
                    margin: 20px 0;
                }
                .btn {
                    display: inline-block;
                    padding: 12px 24px;
                    color: #ffffff;
                    background-color: #007BFF;
                    text-decoration: none;
                    border-radius: 4px;
                    text-align: center;
                    font-size: 16px;
                    margin: 20px auto;
                    display: block;
                    max-width: 200px;
                }
                .btn:hover {
                    background-color: #0056b3;
                }
                .footer {
                    font-size: 12px;
                    color: #999999;
                    text-align: center;
                    margin-top: 30px;
                }
                .footer a {
                    color: #007BFF;
                    text-decoration: none;
                }
                .footer a:hover {
                    text-decoration: underline;
                }
            </style>
            </head>
            <body>
            <div class="container">
                <h1>Welcome to Your E-Course!</h1>
                <p class="content">
                    Hi {{name}},<br><br>
                    Thank you for enrolling in our course! Here are the details of your e-course:
                </p>
                <p class="content">
                    <strong>Course Name:</strong> {{course_name}}<br>
                    <strong>Username:</strong> {{username}}<br>
                    <strong>Password:</strong> {{password}}<br>
                </p>
                <p class="content">
                    Click the button below to access your course materials:
                </p>
                <a href="{{course_access_link}}" class="btn">Access Course</a>
                <p class="content">
                    If you have any questions or need further assistance, please reply to this email or contact our support team.
                </p>
                <p class="content">Happy learning!</p>
                <div class="footer">
                    <p>&copy; Your Company | <a href="https://yourcompany.com">Visit our website</a></p>
                    <p><a href="[Unsubscribe Link]">Unsubscribe</a></p>
                </div>
            </div>
            </body>
            </html>
        """
        html_content = (
            html_template.replace("{{name}}", name)
            .replace("{{course_name}}", course_name)
            .replace("{{username}}", username)
            .replace("{{password}}", password)
            .replace("{{course_access_link}}", course_access_link)
        )
        SubjectPart = "Welcome to {{course_name}}!".replace(
            "{{course_name}}", course_name
        )
        TextPart = "Thank you for enrolling in our e-course!"
        return html_content, SubjectPart, TextPart
