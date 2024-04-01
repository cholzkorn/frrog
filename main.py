import imaplib
import email
import os
from os.path import expanduser

def save_csv_attachment(sender_email, imap_server, imap_username, imap_password):
    # Connect to the email account
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(imap_username, imap_password)
    mail.select("inbox")

    status, messages = mail.search(None, f'(FROM "{sender_email}")')

    if status == "OK":
        email_ids = messages[0].split()
        if email_ids:  # Check if there are any emails from the sender
            newest_email_id = email_ids[-1]  # Get the newest email
            status, msg_data = mail.fetch(newest_email_id, "(RFC822)")

            if status == "OK":
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Process attachments and save the CSV
                for part in msg.walk():
                    if part.get_content_type() == "application/csv":
                        csv_data = part.get_payload(decode=True)

                        # Save csv to home directory
                        filename = 'report.csv'
                        home_directory = expanduser("~")
                        file_path = os.path.join(home_directory, filename)

                        with open(file_path, 'wb') as csv_file:
                            csv_file.write(csv_data)
                        print(f"CSV attachment saved as {file_path}")
                        return file_path
    print("No suitable email found or attachment found.")
    return None

if __name__ == "__main__":
    print(
        """
        Welcome to frrog. Type in the mail account you want to connect to and
        automate the csvs you get from a certain account.
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

    save_csv_attachment(sender_email, imap_server, imap_username, imap_password)