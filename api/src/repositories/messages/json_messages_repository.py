from repositories.messages.messages_repository_interface import MessagesRepositoryInterface
from repositories.json_base_repository import JSONBaseRepository 
from models.message_models import MessageJSONModel
from repositories.users.json_users_repository import JSONUserRepository
from typing import List


class JSONMessageRepository(JSONBaseRepository, MessagesRepositoryInterface):

    def __init__(self) -> None:
        self.users_repository = JSONUserRepository()
        super().__init__(filename="messages.json")


    @property
    def Model(self) -> MessageJSONModel:
        return MessageJSONModel


    def get_chat_messages(self, chat_id:int) -> List[MessageJSONModel]:
        messages = self.get_all()
        chat_messages = []
        for message in messages:
            if message.chat_id == chat_id:
                message.sender_user = self.users_repository.get_by_id(message.sender_user_id)
                chat_messages.append(message)
        return chat_messages
