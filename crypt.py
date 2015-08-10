from Crypto import Random
from Crypto.Cipher import AES

def pad(s):
    return s + b"\0" * ((AES.block_size - len(s)) % AES.block_size)


def encrypt(decrypted, key):
    decrypted = pad(decrypted)
    iv = Random.new().read(AES.block_size) # initialization string
    cipher = AES.new(key, AES.MODE_CBC, iv) # cipher for the encrypting
    return iv + cipher.encrypt(decrypted) # encrypted stuff


def decrypt(encrypted, key):
    iv = encrypted[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(encrypted[AES.block_size:]).rstrip(b"\0")


def encrypt_file(file_name, key):
    crypted = encrypt(open(file_name, 'rb').read(), key)
    open(file_name, 'wb').write(crypted)


def decrypt_file(file_name, key):
    decrypted = decrypt(open(file_name, 'rb').read(), key)
    open(file_name, 'wb').write(decrypted)
