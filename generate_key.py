# generate key.key if does not exist
# and encrypt username and password to file "secret"
import os
from getpass import getpass
from cryptography.fernet import Fernet

key = None
if os.path.exists('key.key'):
    with open('key.key', 'rb') as f:
        key = f.read()

if not key:
    key = Fernet.generate_key()
    with open('key.key', 'wb') as f:
        f.write(key)

f = Fernet(key)
username = f.encrypt(getpass('Username').encode())
password = f.encrypt(getpass('Password').encode())
with open('secret', 'wb') as f:
    f.write(username)
    f.write('\n'.encode())
    f.write(password)