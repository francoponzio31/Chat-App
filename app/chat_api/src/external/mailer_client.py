from config.app_config import config
from requests.exceptions import HTTPError
from utilities.logger import logger
import requests


class MailerClient:
    
    mailer_url = config.MAILER_BASE_URL

    def send_email(self, to_emails: list[str], subject: str, template: str, template_context: dict) -> dict:
        """
        Uploads a file and returns the file id in the mailer.
        """

        url = f"{self.mailer_url}/api/email/send"
        headers = {
            "accept": "application/json",
        }
        body = {
            "to_emails": to_emails,
            "subject": subject,
            "template": template,
            "template_context": template_context
        }
        response = requests.post(url, headers=headers, json=body)

        if not response.ok:
            logger.error(f"Mailer api error response: {response.json()}")
            raise HTTPError

        return response.json()

mailer_client = MailerClient()