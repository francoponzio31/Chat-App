from pydantic import BaseModel, Field, EmailStr


class EmailDataInput(BaseModel):
    to_emails: list[EmailStr] = Field(..., description="List of email addresses of the receivers")
    subject: str = Field(..., description="Subject of the email")
    template: str = Field(..., description="Template for the email body")
    template_context: dict = Field(..., description="Context data for rendering the template")