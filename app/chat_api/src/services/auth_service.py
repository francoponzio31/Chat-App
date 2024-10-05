from repositories.users_repository import users_repository
from utilities.custom_exceptions import InvalidCredentialsError, EmailNotVerifiedError, EmailAlreadyRegisteredError, InvalidVerificationTokenError
from utilities.utils import compare_hashed_password
from integrations.mailer_client import mailer_client
from flask import current_app
import datetime
import jwt
from config.app_config import config


class AuthService:
        
    def login(self, email:str, password:str) -> str:

        user = users_repository.get_by_email(email, raise_if_not_found=False)

        if user and not user.is_verified:
            raise EmailNotVerifiedError

        if not user or not compare_hashed_password(password, user.password):
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


    def signup(self, username:str, email:str, password:str):

        # New user creation
        email_already_registered = users_repository.get_by_email(email, raise_if_not_found=False)
        if email_already_registered:
            raise EmailAlreadyRegisteredError
        
        new_user = users_repository.create_one(username=username, email=email, password=password)

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


    def verify_email(self, user_id:str, token:str):
        user = users_repository.get_by_id(user_id)
        if user.verification_token == token:
            users_repository.update_one(user_id, is_verified=True)
        else:
            raise InvalidVerificationTokenError


    def current_user(self, user_id:int) -> dict:
        return users_repository.get_by_id(user_id)


auth_service = AuthService()