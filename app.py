import os
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO, join_room, emit

from config import Config
from models import db, User, Message


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "warning"

socketio = SocketIO(cors_allowed_origins="*")


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.listing_routes import listing_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.chat_routes import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chat_bp)

    with app.app_context():
        db.create_all()

    return app


@socketio.on("join_chat")
def handle_join_chat(data):
    room = data.get("room")
    join_room(room)


@socketio.on("send_message")
def handle_send_message(data):
    room = data.get("room")
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    listing_id = data.get("listing_id")
    content = data.get("content")

    if not content:
        return

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        listing_id=listing_id,
        content=content
    )

    db.session.add(message)
    db.session.commit()

    emit("receive_message", {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "listing_id": listing_id,
        "content": content,
        "time": message.created_at.strftime("%H:%M")
    }, room=room)


app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)