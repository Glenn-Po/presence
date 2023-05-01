import qrcode
import base64
import io
import os
import cloudinary
import cloudinary.uploader
import cloudinary.utils


def text_to_qr_code_data_uri(text: str) -> str:
    img = qrcode.make(text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_data = buffer.getvalue()
    img_base64 = base64.b64encode(img_data)
    img_str = img_base64.decode("utf-8")
    return "data:image/png;base64," + img_str


def upload_data_uri_to_cloudinary(img_data_uri: str) -> str:
    # configure your cloudinary credentials
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    # upload the data URI to cloudinary
    response = cloudinary.uploader.upload(img_data_uri)

    # get the download URL from the response dictionary
    # download_url = response["url"]

    # or use the cloudinary_url function with the public ID
    download_url, _ = cloudinary.utils.cloudinary_url(
        response["public_id"], format="png")
    return download_url
