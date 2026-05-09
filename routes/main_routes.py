from flask import Blueprint, render_template, request
from models import Listing

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    listings = Listing.query.filter_by(status="active").order_by(Listing.created_at.desc()).all()
    return render_template("index.html", listings=listings)


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").lower()

    listings = Listing.query.filter_by(status="active").all()

    if query:
        listings = [
            l for l in listings
            if query in l.title.lower() or query in l.category.lower()
        ]

    return render_template("index.html", listings=listings)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/safety")
def safety():
    return render_template("safety.html")