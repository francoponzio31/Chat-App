from flask_socketio import SocketIO
from app import create_app
from web_sockets.events import register_socket_events

app = create_app()
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode="gevent",
    logger=True,
    ping_timeout=60,
    ping_interval=25
)

register_socket_events(socketio)

if __name__ == "__main__":
    socketio.run(app, host=app.config["HOST"], port=app.config["PORT"])