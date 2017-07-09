import hashlib
import base64
import os


def encrypt_password(raw_password):
    salt = str(os.urandom(32)).encode('utf-8')
    enc_password = hashlib.sha3_256(salt+raw_password.encode('utf-8')).hexdigest()
    return enc_password, salt


def check_password(raw_password, enc_password, salt):
    to_check = hashlib.sha3_256()
    to_check.update(salt+raw_password)
    if to_check.digest() == enc_password:
        return True
    else:
        return False
