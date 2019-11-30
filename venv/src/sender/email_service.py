import smtplib

email = 'myaddress@gmail.com'
password = 'password'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)


def send_email(email_to: str, detection_id: str, plate: str):
    [camera_id, timestamp] = detection_id.split("-")
    message = f"Found plate {plate} in camera {camera_id} at {timestamp}"
    server.sendmail(email, email_to, message)
    server.quit()
