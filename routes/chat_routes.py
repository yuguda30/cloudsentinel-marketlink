from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, desc

from models import db, User, Listing, Message

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/inbox")
@login_required
def inbox():
    messages = Message.query.filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).order_by(desc(Message.created_at)).all()

    conversations = {}

    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        key = f"{msg.listing_id}-{other_user_id}"

        if key not in conversations:
            other_user = User.query.get(other_user_id)
            conversations[key] = {
                "listing": msg.listing,
                "other_user": other_user,
                "last_message": msg,
                "unread_count": Message.query.filter_by(
                    sender_id=other_user_id,
                    receiver_id=current_user.id,
                    listing_id=msg.listing_id,
                    is_read=False
                ).count()
            }

    return render_template("inbox.html", conversations=conversations.values())


@chat_bp.route("/room/<int:listing_id>/<int:user_id>")
@login_required
def chat_room(listing_id, user_id):
    listing = Listing.query.get_or_404(listing_id)
    other_user = User.query.get_or_404(user_id)

    messages = Message.query.filter(
        Message.listing_id == listing_id,
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()

    Message.query.filter_by(
        sender_id=user_id,
        receiver_id=current_user.id,
        listing_id=listing_id,
        is_read=False
    ).update({"is_read": True})

    db.session.commit()

    room = f"listing-{listing_id}-users-{min(current_user.id, user_id)}-{max(current_user.id, user_id)}"

    return render_template(
        "chat.html",
        listing=listing,
        other_user=other_user,
        messages=messages,
        room=room
    )