from schemas.auth_schema import credentials_schema
from repositories import users_repository
from utilities.custom_exceptions import InvalidCredentials
from utilities.utils import compare_hashed_password
from flask import current_app
import datetime
import jwt


class AuthService:
        
    def login(self, credentials:dict) -> str:

        credentials = credentials_schema.load(credentials)
        user = users_repository.get_by_email(credentials["email"], raise_if_not_found=False)

        if not user or not compare_hashed_password(credentials["password"], user.password):
            raise InvalidCredentials
        
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


auth_service = AuthService()