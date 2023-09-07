
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from ..models import Subscriber, Campaign
import threading
from queue import Queue
import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))

active_subscribers_queue = Queue()


def send_email(subscriber, campaign):
    try:
        # SMTP server configuration (for Mailgun)
        smtp_host = 'smtp.mailgun.org'
        smtp_port = 587  # TLS port

        smtp_username = 'postmaster@.mailgun.org'  # Replace with your SMTP username
        smtp_password = 'smtp_password'  # Replace with your SMTP password


        # Create an SMTP connection
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Load Jinja2 template from the absolute path
        env = Environment(loader=FileSystemLoader(current_directory))
        template = env.get_template('campaign_template.html')

        # Render email content from the template and campaign data
        email_content = template.render(
            subject=campaign.subject,
            preview_text=campaign.preview_text,
            article_url=campaign.article_url,
            html_content=campaign.html_content,
            plain_text_content=campaign.plain_text_content,
            published_date=campaign.published_date.strftime('%Y-%m-%d'),
            recipient_first_name = subscriber.first_name,
        )

        # Create a MIME message
        msg = MIMEMultipart()
        msg['From'] = smtp_username  # Replace with your sender email
        msg['To'] = subscriber.email
        msg['Subject'] = campaign.subject

        # Attach the HTML content to the email
        msg.attach(MIMEText(email_content, 'html'))

        # Send the email
        server.sendmail(smtp_username, subscriber.email, msg.as_string())

        # Quit the SMTP server
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {subscriber.email}: {str(e)}")
    finally:
        active_subscribers_queue.task_done()

def send_emails_in_thread(campaign):
    while True:
        subscriber = active_subscribers_queue.get()
        if subscriber is None:
            # Sentinel value to indicate thread should exit
            active_subscribers_queue.task_done()
            break
        send_email(subscriber, campaign)

def send_latest_campaign_email():
    start_time = datetime.datetime.now()
    try:
        # Retrieve the latest campaign based on the published_date
        latest_campaign = Campaign.objects.latest('published_date')
    except Campaign.DoesNotExist:
        print("No campaigns found in the database.")
        return

    # Retrieve all active subscribers
    active_subscribers = Subscriber.objects.filter(is_active=True)

    # Put active subscribers into the queue
    for subscriber in active_subscribers:
        active_subscribers_queue.put(subscriber)

    num_threads = 5  # Adjust the number of threads as needed
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=send_emails_in_thread, args=(latest_campaign,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    active_subscribers_queue.join()

    for _ in range(num_threads):
        active_subscribers_queue.put(None)

    for thread in threads:
        thread.join()

    end_time = datetime.datetime.now()

    time_difference = end_time - start_time
    print(f"Code execution time: {time_difference}")

    print("All emails sent successfully.")

if __name__ == '__main__':
    send_latest_campaign_email()
