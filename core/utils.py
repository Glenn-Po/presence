import qrcode
import base64
import io
import os
from geopy import distance
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from dotenv import load_dotenv

load_dotenv()


def text_to_qr_code_data_uri(text: str) -> str:
    img = qrcode.make(text)
    buffer = io.BytesIO()
    img.save(buffer)
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

# delete the qr codes whne location is deleted


def delete_image_from_cloudinary(download_url: str) -> None:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )
    public_id = download_url.split('/')[-1].split('.')[0]
    cloudinary.uploader.destroy(public_id)


'''
geoposition: (latitude, longitude)
center: (latitude, longitude)
radius: in metres
'''


def position_within_area(geoposition: tuple[float, float],
                         center:  tuple[float, float],
                         radius) -> bool:
    return distance.distance(geoposition, center).m <= radius
