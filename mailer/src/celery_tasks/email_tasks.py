from celery_app import celery_app
from utilities.logger import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.utils import get_template_content
from config.app_config import config


@celery_app.task
def send_email_task(to_emails: list[str], subject: str, template: str, template_context: dict) -> None:
    msg = MIMEMultipart()
    msg["From"] = config.smtp_username
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    html_content = get_template_content(template, template_context)
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        server = smtplib.SMTP(config.smtp_server, config.smtp_port)
        server.starttls()
        server.login(config.smtp_username, config.smtp_password)
        server.sendmail(config.smtp_username, to_emails, msg.as_string())
        server.quit()
        logger.info("Email sent successfully")
        
    except Exception as e:
        logger.error(f"Exception when sending email: {str(e)}")
        raise
