#! /usr/bin/python



import os
import colorama
import click
from fn import *
import hashlib
from Crypto.Cipher import AES

@click.group()
def commands():
    pass


@click.command()
@click.argument('password')
@click.argument('name')
@click.argument('description', default='')
def write(password: str, name: str, description: str):

    db = read_db()

    # auth

    if len(read_db()[1]) == 0:
        # first time auth

        print(
            colorama.Fore.YELLOW,
            'database is empty'
        )

        print(
            colorama.Style.RESET_ALL,
            colorama.Fore.RED,
            'password is not specified'
        )

        username = input(
            colorama.Fore.YELLOW + 'enter new username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX + 'enter the password for new database (you can use password of any lenght) : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)
        
        # encrypt the test word

        print(
            colorama.Fore.YELLOW,
            'now i will encrypt the database',
            colorama.Style.RESET_ALL
        )

        encrypted_auth = symmetric_encrypt_str('hi', passwd)

        encrypted_password = symmetric_encrypt_str(password, passwd)


        encrypted_description = symmetric_encrypt_str(description, passwd)


        write_to_db(
            [hashlib.sha3_256(username.encode()).hexdigest()],
            {
                'auth' : [encrypted_auth, 'do not change this parameter or you will never can log in'],
                hashlib.sha3_256(name.encode()).hexdigest() : [encrypted_password, encrypted_description]
            }
        )

        print(colorama.Fore.GREEN + 'database encrypted and writed succesfully')

    else:
        username = input(
            colorama.Fore.YELLOW + 'enter new username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX + 'enter the password for new database (you can use password of any lenght) : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN + 'authentication passed, starting to encrypt password')
            
            encrypted_password = symmetric_encrypt_str(password, passwd)

            encrypted_description = symmetric_encrypt_str(description, passwd)

            db[1][ hashlib.sha3_256(name.encode()).hexdigest() ] = [encrypted_password, encrypted_description]

            write_to_db(db[0], db[1])

        else:
            print(colorama.Fore.RED + 'authentication failed, try again')

@click.command()
@click.argument('name')
def read(name):

    db = read_db()

    if len(read_db()[1]) == 0:
        print(colorama.Fore.RED + 'database is empty, there is nothing to read here')
    else:
        username = input(
            colorama.Fore.YELLOW + 'enter new username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX + 'enter the password for new database (you can use password of any lenght) : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN + 'authentication passed, starting to decrypt password')

            try:
                decrypted_password = symmetric_decrypt_bytes(db[1][hashlib.sha3_256(name.encode()).hexdigest()][0], passwd)

                decrypted_description = symmetric_decrypt_bytes(db[1][hashlib.sha3_256(name.encode()).hexdigest()][1], passwd)
            except:
                print(colorama.Fore.RED, 'there is no passwords with same name')
                return
            
            print(colorama.Fore.LIGHTYELLOW_EX, 'password:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_password.decode(), colorama.Fore.LIGHTYELLOW_EX, '\ndescription:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_description.decode())
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')

@click.command()
@click.argument('name')
def remove(name):
    
    db = read_db()

    if len(read_db()[1]) == 0:
        print(colorama.Fore.RED + 'database is empty, there is nothing to remove here')
    else:
        username = input(
            colorama.Fore.YELLOW + 'enter new username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX + 'enter the password for new database (you can use password of any lenght) : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN + 'authentication passed, starting to remove password')

            try:
                db[1].pop(hashlib.sha3_256(name.encode()).hexdigest())
            except:
                print(colorama.Fore.RED, 'there is no passwords with same name for delete them')
                return

            write_to_db(db[0], db[1])

            print(colorama.Fore.GREEN, 'password succesfully removed from the database')
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')

@click.command()
def list_show():
    db = read_db()

    if len(read_db()[1]) == 0:
        print(colorama.Fore.RED + 'database is empty, there is nothing to show here')
    else:
        username = input(
            colorama.Fore.YELLOW + 'enter new username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX + 'enter the password for new database (you can use password of any lenght) : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN, 'authentication passed, starting to count the passwords')
            display = input(colorama.Back.WHITE + colorama.Fore.BLACK + f'there is {len(db[1].items()) - 1} passwords in the database, show them? [y/n]:' + colorama.Back.RESET + ' ' + colorama.Fore.LIGHTMAGENTA_EX)
            if display == 'y':
                for i in db[1].keys():
                    
                    if i != 'auth':
                        decrypted_password = symmetric_decrypt_bytes(db[1][i][0], passwd)

                        decrypted_description = symmetric_decrypt_bytes(db[1][i][1], passwd)

                        print(colorama.Fore.LIGHTYELLOW_EX, 'password:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_password.decode(), colorama.Fore.LIGHTYELLOW_EX, '\ndescription:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_description.decode())

                        print('#' * 40)
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')
        
@click.command()
def version():
    print('version 0.1.0')






commands.add_command(write)
commands.add_command(read)
commands.add_command(remove)
commands.add_command(list_show)
commands.add_command(version)

if __name__ == '__main__':
    commands()
