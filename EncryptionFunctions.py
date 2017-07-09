import hashlib
import os


def encrypt_password(raw_password):
    salt = str(os.urandom(32)).encode('utf-8')
    enc_password = hashlib.sha3_256(salt+raw_password.encode('utf-8')).hexdigest()
    return enc_password, salt


def check_password(raw_password, enc_password, salt):
    to_check = hashlib.sha3_256(salt+raw_password.encode('utf-8')).hexdigest()
    return to_check == enc_password
