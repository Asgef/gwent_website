from firebase_admin import credentials, storage, initialize_app
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
import mimetypes
import os
import json
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

if os.getenv('ADMIN_SDK').startswith('{'):
    cred_dict = json.loads(os.getenv('ADMIN_SDK'))
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate(os.getenv('ADMIN_SDK'))

initialize_app(cred, {
    'storageBucket': os.getenv('URL_SDK_STORAGE')
})

bucket = storage.bucket()


class FirebaseStorage(Storage):
    def __init__(self):
        self.bucket = storage.bucket()

    def _open(self, name, mode='rb'):
        blob = self.bucket.blob(name)
        content = blob.download_as_string()
        return ContentFile(content)

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_file(
            content, content_type=mimetypes.guess_type(name)[0]
        )
        return name

    def delete(self, name):
        blob = self.bucket.blob(name)
        blob.delete()

    def exists(self, name):
        blob = self.bucket.blob(name)
        return blob.exists()

    def url(self, name):
        blob = self.bucket.blob(name)
        url = blob.generate_signed_url(
            expiration=timedelta(hours=1),
            method='GET'
        )
        return url

    def size(self, name):
        blob = self.bucket.blob(name)
        return blob.size

    def _get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name
