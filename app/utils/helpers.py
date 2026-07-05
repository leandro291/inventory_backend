import base64
import os
from typing import Union
import bcrypt
import cloudinary
import cloudinary.uploader
from cryptography.fernet import Fernet
from werkzeug.datastructures import FileStorage

class PasswordHelper:

    def hash_password(self, password: str) -> str:
        bytes_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes_password, salt)
        return hashed_password.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> str:
        bytes_password = password.encode('utf-8')
        bytes_hash_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(bytes_password, bytes_hash_password)

class CryptoHelper:
    def __init__(self):
        self._key = os.getenv('FERNET_SECRET_KEY')
        self.validate_key()
        self.fernet = Fernet(self._key)

    def encrypt(self, value: Union[str, int, float, bool]) -> str:
        string_value = str(value)
        bytes_value = string_value.encode('utf-8')
        encrpyted_value = self.fernet.encrypt(bytes_value)
        return encrpyted_value.decode('utf-8')

    def decrypt(self, value: str) -> Union[str, int, float, bool]:
        bytes_value = value.encode('utf-8')
        decrypted_value = self.fernet.decrypt(bytes_value)
        return decrypted_value.decode('utf-8')
    
    def validate_key(self):
        if not self._key:
            raise ValueError('FERNET_SECRET_KEY is not set')
        
        try:
            bytes_key = base64.urlsafe_b64decode(self._key)

            if len(bytes_key) != 32:
                raise ValueError('Invalid key length')
        except ValueError as e:
            raise ValueError(f'{e}')
        
class CloudinaryHelper:
    def __init__(self):
        cloudinary.config( 
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
            api_key = os.getenv('CLOUDINARY_API_KEY'), 
            api_secret = os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

    def upload_image(self, image: FileStorage, folder: str = "products") -> tuple:
        try:
            response = cloudinary.uploader.upload(
                image,
                folder=folder
            )

            secure_url = response.get('secure_url')
            public_id = response.get('public_id')

            return secure_url, public_id
        except Exception as e:
            return None, None
        
    def get_secure_url(self, public_id: str) -> str:
        try:
            
            secure_url = cloudinary.utils.cloudinary_url(
                public_id,
                secure=True
            )

            return secure_url[0]

        except Exception as e:
            return None
        
    def delete_image(self, public_id: str) -> bool:
        try:
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception as e:
            return False
        
    def validate_image(self, image: FileStorage) -> bool | tuple[bool, str]:

        if not image:
            raise Exception("Image is required")
        
        if image.filename == "":
            raise Exception("Image is required")
        
        if not image.content_type.startswith("image/"):
            raise Exception("Invalid image type")
    
crypto_helper = CryptoHelper()
password_helper = PasswordHelper()
cloudinary_helper = CloudinaryHelper()
