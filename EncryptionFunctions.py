import hashlib
import os
import redis
import secrets

token_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def encrypt_password(raw_password):
    salt = str(os.urandom(32)).encode('utf-8')
    enc_password = hashlib.sha3_256(salt+raw_password.encode('utf-8')).hexdigest()
    return enc_password, salt


def check_password(raw_password, enc_password, salt):
    to_check = hashlib.sha3_256(salt+raw_password.encode('utf-8')).hexdigest()
    return to_check == enc_password


def authenticate(token):
    if token is not None:
        return token_db.get(token.encode('utf-8')) is not None
    return False


def retrieve_username(token):
    return token_db.get(token).decode('utf-8')


def generate_session_token(username):
    session_token = secrets.token_urlsafe()
    token_db.setex(session_token.encode('utf-8'), 86400, username.encode('utf-8'))  # 24-hour expiration
    return session_token


def delete_session_token(token):
    token_db.delete(token.encode('utf-8'))
