import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "peauriko@gmail.com"  # Enter your address
receiver_email = "peauriko@gmail.com"  # Enter receiver address
password = "Kirjolohi1"
message = """\
Subject: Hi there

This message is sent from Python.""".encode("utf-8")

context = ssl.create_default_context()
def sendEmail(message):
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

