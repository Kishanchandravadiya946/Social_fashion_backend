import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from config import CloudinaryUpload

cloudinary.config(
    cloud_name = CloudinaryUpload.cloud_name, 
    api_key =CloudinaryUpload.api_key, 
    api_secret =CloudinaryUpload.api_secret, 
    secure=CloudinaryUpload.secure
)

def uploadfie(file,name=None):
    upload_result = cloudinary.uploader.upload(file,public_id=name)
    print(upload_result['secure_url'])
    