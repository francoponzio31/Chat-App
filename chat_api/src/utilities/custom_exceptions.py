class EntityNotFoundError(Exception): pass

class InvalidCredentialsError(Exception): pass

class EmailNotVerifiedError(Exception): pass

class EmailAlreadyRegisteredError(Exception): pass

class IsGroupModificationError(Exception): pass

class GroupNameModificationError(Exception): pass

class ContactAlreadyRegisteredError(Exception): pass

class MemberAlreadyInChatError(Exception): pass

class UserIsNotInChatError(Exception): pass
