import os
from typing import List, Dict, Union
import pickle
import hashlib
from Crypto.Cipher import AES


def get_path() -> Union[str, bool]:
    '''
    return database path if exists
    '''

    if os.path.exists(os.path.join(os.getcwd(), 'database')):
        return os.path.join(os.getcwd(), 'database')
    else:
        return False


def pad(somestr: bytes)-> bytes:
    '''
    returns bytes string with len = 16 for encrypting    
    '''

    return somestr + b' ' * (16 - len(somestr) % 16)


def write_to_db(users: List, data: Dict):
    '''
    write to database your files
    '''
    with open(get_path(), 'wb') as file:
        pickle.dump(users, file)
        pickle.dump(data, file)

def write_backup(filename: str, users: List, data: Dict, time: str):
    '''
    write backups of the database
    '''
    with open(os.path.join(os.getcwd(), 'backups/' + filename) , 'wb') as file:
        pickle.dump(users, file)
        pickle.dump(data, file)
        pickle.dump(time, file)

def read_db()-> List:
    '''
    returns list of users and data dictionary in list
    [users: list, data: dict]
    '''
    try:
        with open(get_path(), 'rb') as file:
            return [pickle.load(file), pickle.load(file)]
    except:
        return [[], {}]

def read_backup(filename: str)-> List:
    '''
    returns list of users and data dictionary in list
    [users: list, data: dict, time: str]
    '''
    try:
        with open(os.path.join(os.getcwd(), 'backups/' + filename), 'rb') as file:
            return [pickle.load(file), pickle.load(file), pickle.load(file)]
    except:
        return [[], {}, '']



# добавление нескольких пробелов в конец байтовой строки чтобы ее длина была кратна 16
transform_password = lambda password_str : password_str + b' ' * (16 - len(password_str) % 16)


# шифрование обычной строки симметричным шифром
symmetric_encrypt_str = lambda message, key : AES.new(transform_password(key.encode())[  :16], AES.MODE_CTR, nonce=b'0' * 8).encrypt(message.encode())


# шифрование байтовой строки симметричным шифром
symmetric_encrypt_bytes = lambda message, key : AES.new(transform_password(key.encode())[  :16], AES.MODE_CTR, nonce=b'0' * 8).encrypt(message)



# дешифрование обычной строки симметричным шифром
symmetric_decrypt_str = lambda message, key : AES.new(transform_password(key.encode())[  :16], AES.MODE_CTR, nonce=b'0' * 8).decrypt(message.encode())

# дешифрование байтовой строки симметричным шифром
symmetric_decrypt_bytes = lambda message, key : AES.new(transform_password(key.encode())[  :16], AES.MODE_CTR, nonce=b'0' * 8).decrypt(message)





# хеширование пароля  100 раз просто для дополнительной безопасности
def hash_100(password: str) -> str:
    for i in range(100):
        password = hashlib.sha3_256(password.encode()).hexdigest()
    return password


# example:
# symmetric_decrypt_bytes(
#     symmetric_encrypt_bytes(
#         b'hi',
#         hash_100('password'),
#     ),
#     hash_100('password')
# )