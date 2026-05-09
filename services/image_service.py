import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def validate_image(file):
    if not file or file.filename == "":
        return False, "Please upload a product image."

    if not allowed_file(file.filename):
        return False, "Only JPG, JPEG, and PNG images are allowed."

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    max_size = current_app.config["MAX_IMAGE_SIZE"]

    if file_size > max_size:
        return False, "Image is too large. Maximum allowed size is 1MB."

    try:
        image = Image.open(file)
        image.verify()
        file.seek(0)
    except Exception:
        return False, "Invalid image file. Please upload a valid image."

    return True, "Image is valid."


def save_listing_image(file):
    is_valid, message = validate_image(file)

    if not is_valid:
        return None, message

    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit(".", 1)[1].lower()

    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    return unique_filename, "Image uploaded successfully."


def delete_listing_image(filename):
    if not filename:
        return False

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return True

    return False