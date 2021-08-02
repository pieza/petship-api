import bcrypt

def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def check_password(hashStr, password: str):
    return bcrypt.checkpw(password.encode('utf8'), hashStr)

