from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from dataclasses import dataclass
import smtplib


@dataclass
class EmailInitializer:
    message: MIMEMultipart
    body: MIMEText
    subject: str
    sender: str
    receiver: str
    attachments: None | list[MIMEImage | MIMEAudio | MIMEApplication] = None


@dataclass
class SMTPInitializer:
    sender: str
    password: str
    receiver: str


class EmailService:
    def __init__(self, email_info: EmailInitializer, smtp_info: SMTPInitializer):
        self.email_info = email_info
        self.smtp_info = smtp_info

    def __assemble_message(self) -> MIMEMultipart:
        self.email_info.message['Subject'] = self.email_info.subject
        self.email_info.message['From'] = self.email_info.sender
        self.email_info.message['To'] = self.email_info.receiver
        self.email_info.message.attach(self.email_info.body)

        if self.email_info.attachments is not None:
            for attachment in self.email_info.attachments:
                self.email_info.message.attach(attachment)
        return self.email_info.message

    def send_email(self):
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as smtp:
            smtp.login(self.smtp_info.sender, self.smtp_info.password)
            smtp.send_message(
                msg=self.__assemble_message(),
                from_addr=self.smtp_info.sender,
                to_addrs=self.smtp_info.receiver
            )
