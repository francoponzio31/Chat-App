from flask_socketio import SocketIO, join_room, emit
from utilities.logger import logger
from auth.auth import decode_token
from schemas.chat_schemas import message_output_schema
from schemas.sockets_schemas import join_chat_event_schema, create_chat_event_schema, chat_created_event_schema
from services.chats_service import chats_service
from marshmallow import ValidationError
from utilities.custom_exceptions import AuthenticationFailedError, UserIsNotInChatError


def check_authentication(token: str) -> dict:
    try:
        data = decode_token(token)
        return data
    except Exception as ex:
        logger.error(f"Authentication failed: {ex}")
        raise AuthenticationFailedError


def check_if_user_is_in_chat(chat_id: int, user_id: int):
    if not chats_service.check_if_user_is_in_chat(chat_id, user_id):
        raise UserIsNotInChatError


def handle_connect(auth):
    try:
        user_data = check_authentication(auth.get("token", ""))
        user_id = user_data["user"]["id"]

        # Join user to their chat rooms
        user_chats, _ = chats_service.get_user_chats(user_id)
        for chat in user_chats:
            join_room(chat.id)

        logger.info(f"User {user_id} connected and joined chat rooms")
        emit("connected")
    except AuthenticationFailedError:
        logger.warning("Client authentication failed")
        return
    except Exception as ex:
        logger.error(f"Error connecting user_id: {ex}")
        return


def handle_disconnect():
    try:
        logger.info("Client disconnected")
    except Exception as ex:
        logger.error(f"Error disconnecting user_id: {ex}")


def handle_join_chat(data: dict):
    try:
        user_data = check_authentication(data.get("token", ""))
        user_id = user_data["user"]["id"]
        event_detail =  join_chat_event_schema.load(data.get("detail", {}))
        check_if_user_is_in_chat(event_detail["chat_id"], user_id)
        join_room(event_detail["chat_id"])
        logger.info(f"User {repr(user_id)} joined chat room: {repr(event_detail['chat_id'])}")
    except ValidationError as ex:
        logger.error(f"Error validating event detail: {ex.messages}")
    except UserIsNotInChatError:
        logger.warning(f"User {user_id} is not in chat {data['chat_id']}")
    except Exception as ex:
        logger.error(f"Error joining chat: {ex}")


def handle_send_message(data: dict):
    try:
        check_authentication(data.get("token", ""))
        new_message = message_output_schema.load(data.get("message", {}))
        check_if_user_is_in_chat(new_message["chat_id"], new_message["sender_user"]["id"])
        emit("new_message", message_output_schema.dump(new_message), room=new_message["chat_id"])
        logger.info(f"Successfully emitted new_message event for user {repr(new_message['sender_user']['id'])} in chat room {repr(new_message['chat_id'])}")
    except ValidationError as ex:
        logger.error(f"Error validating event detail: {ex.messages}")
    except UserIsNotInChatError:
        logger.warning(f"User {new_message['sender_user']['id']} is not in chat {new_message['chat_id']}")
    except Exception as ex:
        logger.error(f"Error in handle_send_message: {ex}")
        emit("error", {"message": "Failed to send message notification"})


def handle_create_chat(data: dict):
    try:
        check_authentication(data.get("token", ""))
        event_detail = create_chat_event_schema.load(data.get("detail", {}))
        emit("chat_created", chat_created_event_schema.dump(event_detail), broadcast=True)
        logger.info(f"Chat created {event_detail['chat_id']}")
    except ValidationError as ex:
        logger.error(f"Error validating event detail: {ex.messages}")
    except Exception as ex:
        logger.error(f"Error creating chat: {ex}")
        emit("error", {"message": "Failed to create chat"})


def register_socket_events(socketio: SocketIO):
    socketio.on_event("connect", handle_connect)
    socketio.on_event("disconnect", handle_disconnect)
    socketio.on_event("join_chat", handle_join_chat)
    socketio.on_event("send_message", handle_send_message)
    socketio.on_event("create_chat", handle_create_chat)
