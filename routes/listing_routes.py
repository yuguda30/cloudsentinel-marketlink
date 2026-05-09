from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Listing
from services.image_service import save_listing_image, delete_listing_image
from services.location_service import get_states, get_lgas_by_state, is_valid_state_lga

listing_bp = Blueprint("listing", __name__, url_prefix="/listing")


@listing_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_listing():
    states = get_states()

    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        condition = request.form.get("condition")
        price = request.form.get("price")
        state = request.form.get("state")
        lga = request.form.get("lga")
        description = request.form.get("description")
        phone = request.form.get("phone")
        image = request.files.get("image")

        if not is_valid_state_lga(state, lga):
            flash("Invalid location selected.", "danger")
            return redirect(url_for("listing.new_listing"))

        filename, message = save_listing_image(image)
        if not filename:
            flash(message, "danger")
            return redirect(url_for("listing.new_listing"))

        listing = Listing(
            seller_id=current_user.id,
            title=title,
            category=category,
            condition=condition,
            price=float(price),
            state=state,
            lga=lga,
            description=description,
            image_filename=filename,
            contact_phone=phone
        )

        db.session.add(listing)
        db.session.commit()

        flash("Listing posted successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("post_listing.html", states=states)


@listing_bp.route("/<int:id>")
def detail(id):
    listing = Listing.query.get_or_404(id)

    if listing.status != "active":
        flash("Listing not available.", "warning")
        return redirect(url_for("main.home"))

    listing.views += 1
    db.session.commit()

    return render_template("product_detail.html", listing=listing)


# ✅ EDIT LISTING (NEW)
@listing_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_listing(id):
    listing = Listing.query.get_or_404(id)
    states = get_states()

    if listing.seller_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.category = request.form.get("category")
        listing.condition = request.form.get("condition")
        listing.price = float(request.form.get("price"))
        listing.state = request.form.get("state")
        listing.lga = request.form.get("lga")
        listing.description = request.form.get("description")
        listing.contact_phone = request.form.get("phone")

        image = request.files.get("image")
        if image and image.filename != "":
            delete_listing_image(listing.image_filename)
            filename, message = save_listing_image(image)

            if not filename:
                flash(message, "danger")
                return redirect(url_for("listing.edit_listing", id=id))

            listing.image_filename = filename

        db.session.commit()

        flash("Listing updated successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("edit_listing.html", listing=listing, states=states)


@listing_bp.route("/delete/<int:id>")
@login_required
def delete_listing(id):
    listing = Listing.query.get_or_404(id)

    if listing.seller_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.home"))

    delete_listing_image(listing.image_filename)

    db.session.delete(listing)
    db.session.commit()

    flash("Listing deleted.", "info")
    return redirect(url_for("dashboard.dashboard"))


@listing_bp.route("/mark-sold/<int:id>")
@login_required
def mark_sold(id):
    listing = Listing.query.get_or_404(id)

    if listing.seller_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.home"))

    listing.status = "sold"
    db.session.commit()

    flash("Marked as sold.", "success")
    return redirect(url_for("dashboard.dashboard"))


# ✅ LGA API FIX (VERY IMPORTANT)
@listing_bp.route("/lgas/<state>")
def get_lgas(state):
    lgas = get_lgas_by_state(state)
    return jsonify(lgas)