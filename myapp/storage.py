import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.conf import settings
import os

class CloudinaryStorage(Storage):
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        )

    def _save(self, name, content):
        public_id = os.path.splitext(name)[0]
        response = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
        )
        return response['secure_url']

    def url(self, name):
        return name

    def exists(self, name):
        return False

    def delete(self, name):
        try:
            public_id = name.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        except:
            pass