from config.app_config import config


data_persistence_type = config.DATA_PERSISTENCE_TYPE

if data_persistence_type == "JSON":
    from repositories.chats.json_chats_repository import JSONChatRepository
    from repositories.contacts.json_contacts_repository import JSONContactRepository
    from repositories.users.json_users_repository import JSONUserRepository
    from repositories.chat_members.json_chat_members_repository import JSONChatMemberRepository
    from repositories.messages.json_messages_repository import JSONMessageRepository

    users_repository = JSONUserRepository()
    chats_repository = JSONChatRepository()
    contacts_repository = JSONContactRepository()
    chat_members_repository = JSONChatMemberRepository()
    messages_repository = JSONMessageRepository()
    

elif data_persistence_type == "SQL":
    from repositories.users.sql_users_repository import SQLUserRepository
    from repositories.chats.sql_chats_repository import SQLChatRepository
    from repositories.contacts.sql_contacts_repository import SQLContactRepository
    from repositories.chat_members.sql_chat_members_repository import SQLChatMemberRepository
    from repositories.messages.sql_messages_repository import SQLMessageRepository

    users_repository = SQLUserRepository()
    chats_repository = SQLChatRepository()
    contacts_repository = SQLContactRepository()
    chat_members_repository = SQLChatMemberRepository()
    messages_repository = SQLMessageRepository()
