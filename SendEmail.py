import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
    
def send_email(subject, to_email, html_content_body):
    sender_email='shardcdemo@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = 'shardcdemo@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = subject 
   
    msg.attach(MIMEText(html_content_body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, 'rstk voic fesm yhnz')
            server.send_message(msg)
        print(f'Email sent successfully to {to_email}')
    except Exception as e:
        print(f'An error occurred while sending email: {e}')