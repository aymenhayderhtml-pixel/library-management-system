from passlib.hash import bcrypt_sha256 as bcrypt
def hash_password(password: str) -> str:
    return bcrypt.hash(password)
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)