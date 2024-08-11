from schemas.auth_schema import credentials_schema, email_validation_schema, current_user_schema
from schemas.user_schema import user_schema
from repositories import users_repository
from utilities.custom_exceptions import InvalidCredentialsError, EmailNotVerifiedError, EmailAlreadyRegisteredError, InvalidVerificationTokenError
from utilities.utils import compare_hashed_password
from integrations.mailer_client import mailer_client
from flask import current_app
import datetime
import jwt
from config.app_config import config


class AuthService:
        
    def login(self, credentials:dict) -> str:

        credentials = credentials_schema.load(credentials)
        user = users_repository.get_by_email(credentials["email"], raise_if_not_found=False)

        if not user.is_verified:
            raise EmailNotVerifiedError

        if not user or not compare_hashed_password(credentials["password"], user.password):
            raise InvalidCredentialsError

        payload = {
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            },
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(hours=8),  # Token valid for 8 hours
        }

        token = jwt.encode(payload, current_app.config["JWT_KEY"], algorithm="HS256")

        return token


    def signup(self, new_user_data:dict):

        # New user creation
        new_user_data = user_schema.load(new_user_data)

        email_already_registered = users_repository.get_by_email(new_user_data["email"], raise_if_not_found=False)
        if email_already_registered:
            raise EmailAlreadyRegisteredError
        
        new_user = users_repository.create_one(new_user_data)

        # Verification email sending
        mailer_client.send_email(
            to_emails=[new_user.email],
            subject="Chat app email verification",
            template="validate_signup.html",
            template_context={
                "user_id": new_user.id,
                "username": new_user.username,
                "app_client_url": config.CLIENT_BASE_URL,
                "verification_token": new_user.verification_token
            }
        )


    def verify_email(self, email_validation_data:dict):
        email_validation_data = email_validation_schema.load(email_validation_data)
        user_id = email_validation_data["user_id"]
        verification_token = email_validation_data["token"]

        user = users_repository.get_by_id(user_id)
        if user.verification_token == verification_token:
            users_repository.update_one(user_id, {"is_verified": True})
        else:
            raise InvalidVerificationTokenError


    def current_user(self, user_id:int) -> dict:
        user = users_repository.get_by_id(user_id)
        return current_user_schema.dump(user)


auth_service = AuthService()