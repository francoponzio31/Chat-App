
from schemas.inputs import EmailDataInput
from celery_tasks.email_tasks import send_email_task
from utilities.logger import logger


class EmailsService:

    async def send_email(self, email_data:EmailDataInput) -> None:
        send_email_task.delay(
            to_emails=email_data.to_emails,
            subject=email_data.subject,
            template=email_data.template,
            template_context=email_data.template_context
        )
        logger.info("Email task queued successfully")

emails_service = EmailsService()
