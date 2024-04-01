import imaplib
import email
import os
import requests
from os.path import expanduser
from datetime import datetime, timedelta

def process_email_text(text):
    # Send mail text to API for task conversion
    api_url = "http://your_task_conversion_api_endpoint"
    response = requests.post(api_url, json={"email_text": text})
    if response.status_code == 200:
        tasks = response.json()["tasks"]
        print("Tasks generated:", tasks)
    else:
        print("Failed to process email text:", response.text)

def process_csv_attachment(csv_data):
    # Send CSV data to API for visualization conversion
    api_url = "http://your_visualization_conversion_api_endpoint"
    files = {'file': csv_data}
    response = requests.post(api_url, files=files)
    if response.status_code == 200:
        visualization_url = response.json()["visualization_url"]
        print("Visualization URL:", visualization_url)
    else:
        print("Failed to process CSV attachment:", response.text)

def save_attachments(sender_email, imap_server, imap_username, imap_password, days_back):
    # Connect to the email account
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(imap_username, imap_password)
    mail.select("inbox")

    # Define search criteria with date range
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%d-%b-%Y')
    end_date = datetime.now().strftime('%d-%b-%Y')
    search_criteria = f'(FROM "{sender_email}") (SINCE "{start_date}") (BEFORE "{end_date}")'

    status, messages = mail.search(None, search_criteria)

    if status == "OK":
        email_ids = messages[0].split()
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            if status == "OK":
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Process email text
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        email_text = part.get_payload()
                        process_email_text(email_text)

                # Process attachments
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "application/csv" or content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                        attachment_data = part.get_payload(decode=True)
                        if content_type == "application/csv":
                            process_csv_attachment(attachment_data)
                        else:
                            print("Unsupported attachment format:", content_type)

    mail.close()
    mail.logout()

if __name__ == "__main__":
    print(
        """
        Welcome to frrog. Type in the mail account you want to connect to and
        automate the processing of emails and attachments from a certain account within a given timeframe.
        """
    )
    print('Your IMAP server: ')
    imap_server = input()
    print('Your IMAP username: ')
    imap_username = input()
    print('Your IMAP password: ')
    imap_password = input()
    print('Sender mail: ')
    sender_email = input()
    print('How many days back would you like to search? ')
    days_back = int(input())

    save_attachments(sender_email, imap_server, imap_username, imap_password, days_back)
