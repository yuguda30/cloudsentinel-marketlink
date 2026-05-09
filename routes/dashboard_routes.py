from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Listing

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def dashboard():
    listings = Listing.query.filter_by(
        seller_id=current_user.id
    ).order_by(
        Listing.created_at.desc()
    ).all()

    active_count = len([listing for listing in listings if listing.status == "active"])
    sold_count = len([listing for listing in listings if listing.status == "sold"])
    total_views = sum(listing.views for listing in listings)

    return render_template(
        "dashboard.html",
        listings=listings,
        active_count=active_count,
        sold_count=sold_count,
        total_views=total_views
    )