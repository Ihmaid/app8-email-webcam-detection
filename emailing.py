import smtplib
import imghdr
from email.message import EmailMessage

# App password of the defined email
PASSWORD = "vfvr iwes xadb jeqr"
SENDER = "teste1111python@gmail.com"
RECEIVER = "teste1111python@gmail.com"


# Function to send an email when triggered
def send_email(image_path):
    # Creates and EmailMessage object
    email_message = EmailMessage()
    email_message["Subject"] = "New costumer showed up!"
    email_message.set_content("Hey, we just saw a new costumer")

    # Read the image and store it at the var content
    with open(image_path, "rb") as file:
        content = file.read()
    # Method of EmailMessage class to add an attachment into email body
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))

    # Pattern to initiate the gmail server and requests
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    # Function to send the email
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/84.png")
