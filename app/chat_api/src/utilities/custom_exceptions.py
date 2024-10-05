class EntityNotFoundError(Exception): pass

class InvalidCredentialsError(Exception): pass

class EmailNotVerifiedError(Exception): pass

class EmailAlreadyRegisteredError(Exception): pass

class InvalidVerificationTokenError(Exception): pass

class MemberAlreadyInChatError(Exception): pass

class UserIsNotInChatError(Exception): pass

class DirectChatWithSameUserError(Exception): pass
