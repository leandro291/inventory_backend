import secrets
from cryptography.fernet import Fernet

key = Fernet.generate_key()
llave_flask = secrets.token_hex(32)
llave_jwt = secrets.token_hex(32)

print(f"FERNET_SECRET_KEY: {key.decode()}")
print(f"SECRET_KEY= {llave_flask}")
print(f"JWT_SECRET_KEY= {llave_jwt}")