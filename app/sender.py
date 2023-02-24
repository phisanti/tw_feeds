import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import make_msgid

def make_msgid_list(n):
    
    """ Generate a list of make_msgid() for images
    :param n: number of images
    :return: list of image ids
    """
    n=n+1
    attachmets_ids=[make_msgid('image{}'.format(i)) for i in range(1,n)]
    return attachmets_ids

def send_newsletter(email_config, email_path, attachment_cid) -> dict:

    """ Send email with the html file built previously.
    :param email_config: Dictionary with the email settings, maily, password, sender email and receiver email.
    :param email_path: Directory to the HTML email file.
    :param attachment_cid: placeholder to locate attached images.
    """
    # Config email
    sender_email = email_config['SENDER_EMAIL']
    receiver_email = email_config['RECEIVER_EMAIL']
    password = email_config['EMAIL_PASSWORD']

    email = EmailMessage()
    email ["Subject"] = "multipart test day: {}".format(datetime.today().date())
    email ["From"] = sender_email
    email ["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    with open(email_path, "rb") as attachment:
        email_html = BeautifulSoup(attachment.read(), 'html.parser')
        email.set_content(str(email_html), subtype="html")
    
    with open('app/dataplots/words.png', 'rb') as fp:
        email.add_related(fp.read(), 'image1', 'png', cid=attachment_cid[0])
    with open('app/dataplots/sentiment.png', 'rb') as fp:
        email.add_related(fp.read(), 'image2', 'png', cid=attachment_cid[1])
    with open('app/dataplots/polarity.png', 'rb') as fp:
        email.add_related(fp.read(), 'image3', 'png', cid=attachment_cid[2])
    with open('app/dataplots/heatmap.png', 'rb') as fp:
        email.add_related(fp.read(), 'image3', 'png', cid=attachment_cid[3])
    
    server = smtplib.SMTP('smtp.office365.com', 587)  ### put your relevant SMTP here
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)  ### if applicable
    server.send_message(email)
    server.quit()
    
    return True

def send_newsletter_from_ram(email_config, email_html, attachment_cid) -> dict:

    """ Send email with the html file built previously.
    :param email_config: Dictionary with the email settings, maily, password, sender email and receiver email.
    :param email_html: HTML object with the newsletter.
    :param attachment_cid: placeholder to locate attached images.
    :return: True if the email was sent.
    """
    # Config email
    sender_email = email_config['SENDER_EMAIL']
    receiver_email = email_config['RECEIVER_EMAIL']
    password = email_config['EMAIL_PASSWORD']

    email = EmailMessage()
    email["Subject"] = "multipart test day: {}".format(datetime.today().date())
    email["From"] = sender_email
    email["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    email.set_content(email_html.render(), subtype="html")
    with open('app/dataplots/words.png', 'rb') as fp:
        email.add_related(fp.read(), 'image1', 'png', cid=attachment_cid[0])
    with open('app/dataplots/sentiment.png', 'rb') as fp:
        email.add_related(fp.read(), 'image2', 'png', cid=attachment_cid[1])
    with open('app/dataplots/polarity.png', 'rb') as fp:
        email.add_related(fp.read(), 'image3', 'png', cid=attachment_cid[2])
    with open('app/dataplots/heatmap.png', 'rb') as fp:
        email.add_related(fp.read(), 'image3', 'png', cid=attachment_cid[3])
    
    server = smtplib.SMTP('smtp.office365.com', 587)  ### put your relevant SMTP here
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)  ### if applicable
    server.send_message(email)
    server.quit()
    
    return True

#send_newsletter(config, email_path="test.html", attachment_cid=attachment_cid)
#send_newsletter_from_ram(config, email_html=email, attachment_cid=attachment_cid)
#send_newsletter(config, 'test.html', attachment_cid)

#with open('test.html', 'w') as f:
#    f.write(email.render())