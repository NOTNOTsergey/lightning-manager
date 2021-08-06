#! /usr/bin/python


import os
import colorama
import click
from fn import *
import hashlib
from Crypto.Cipher import AES
import time


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
            colorama.Fore.LIGHTYELLOW_EX +
            'enter the password for new database (you can use password of any lenght) : ' +
            colorama.Fore.LIGHTBLUE_EX
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
                'auth': [encrypted_auth, 'do not change this parameter or you will never can log in'],
                hashlib.sha3_256(name.encode()).hexdigest(): [encrypted_password, encrypted_description]
            }
        )

        print(colorama.Fore.GREEN + 'database encrypted and writed succesfully')

    else:
        username = input(
            colorama.Fore.YELLOW + 'enter the username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX +
            'enter the password for database : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN +
                  'authentication passed, starting to encrypt password')

            encrypted_password = symmetric_encrypt_str(password, passwd)

            encrypted_description = symmetric_encrypt_str(description, passwd)

            db[1][hashlib.sha3_256(name.encode()).hexdigest()] = [
                encrypted_password, encrypted_description]

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
            colorama.Fore.YELLOW + 'enter the username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX +
            'enter the password for database : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN +
                  'authentication passed, starting to decrypt password')

            try:
                decrypted_password = symmetric_decrypt_bytes(
                    db[1][hashlib.sha3_256(name.encode()).hexdigest()][0], passwd)

                decrypted_description = symmetric_decrypt_bytes(
                    db[1][hashlib.sha3_256(name.encode()).hexdigest()][1], passwd)
            except:
                print(colorama.Fore.RED, 'there is no passwords with same name')
                return

            print(colorama.Fore.LIGHTYELLOW_EX, 'password:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_password.decode(
            ), colorama.Fore.LIGHTYELLOW_EX, '\ndescription:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_description.decode())
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')


@click.command()
@click.argument('name')
def remove(name):

    db = read_db()

    if len(read_db()[1]) == 0:
        print(colorama.Fore.RED +
              'database is empty, there is nothing to remove here')
    else:
        username = input(
            colorama.Fore.YELLOW + 'enter the username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX +
            'enter the password for database : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN +
                  'authentication passed, starting to remove password')

            try:
                db[1].pop(hashlib.sha3_256(name.encode()).hexdigest())
            except:
                print(colorama.Fore.RED,
                      'there is no passwords with same name for delete them')
                return

            write_to_db(db[0], db[1])

            print(colorama.Fore.GREEN,
                  'password succesfully removed from the database')
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')


@click.command()
def list_show():
    db = read_db()

    if len(read_db()[1]) == 0:
        print(colorama.Fore.RED + 'database is empty, there is nothing to show here')
    else:
        username = input(
            colorama.Fore.YELLOW + 'enter the username : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = input(
            colorama.Fore.LIGHTYELLOW_EX +
            'enter the password for database : ' + colorama.Fore.LIGHTBLUE_EX
        )

        passwd = hash_100(passwd)

        if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
            print(colorama.Fore.GREEN,
                  'authentication passed, starting to count the passwords')
            display = input(colorama.Back.WHITE + colorama.Fore.BLACK +
                            f'there is {len(db[1].items()) - 1} passwords in the database, show them? [y/n]:' + colorama.Back.RESET + ' ' + colorama.Fore.LIGHTMAGENTA_EX)
            if display == 'y':
                for i in db[1].keys():

                    if i != 'auth':
                        decrypted_password = symmetric_decrypt_bytes(
                            db[1][i][0], passwd)

                        decrypted_description = symmetric_decrypt_bytes(
                            db[1][i][1], passwd)

                        print(colorama.Fore.LIGHTYELLOW_EX, 'password:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_password.decode(
                        ), colorama.Fore.LIGHTYELLOW_EX, '\ndescription:\n', colorama.Fore.LIGHTMAGENTA_EX, decrypted_description.decode())

                        print('#' * 40)
        else:
            print(colorama.Fore.RED + 'authentication failed, try again')


@click.command()
@click.option('--dates', default=False, help='show backups dates and NOT write new backup')
def backup(dates):

    db = read_db()

    if not os.path.exists(os.path.join(os.getcwd(), 'backups')):
        os.mkdir('backups')

    if dates:
        if len(os.listdir("./backups")) != 1:
            print(colorama.Fore.YELLOW,
                  f'there is {len(os.listdir("./backups"))} backups', '\ndates:\n', sep='')
        else:
            print(colorama.Fore.YELLOW,
                  f'there is only 1 backup', '\ndate:\n', sep='')

        i = 1

        for i in os.listdir('./backups'):

            print(colorama.Fore.LIGHTCYAN_EX, i, colorama.Fore.BLUE, ' : ',
                  colorama.Fore.LIGHTMAGENTA_EX, read_backup(i)[2], sep='')
    elif len(os.listdir('./backups')) >= 5:
        print(colorama.Fore.RED,
              'backups number is larger then 5, i will remove and replace old backups')

        backups = [i for i in map(str, sorted(
            [i for i in map(int, os.listdir('./backups'))]))]

        for i in range(4, len(backups)):
            os.remove(os.path.join(os.path.abspath(
                ''), 'backups/' + backups[i]))

        print(colorama.Fore.GREEN, 'backups removed and replaced')

        write_backup(str(int(time.time())), db[0], db[1], time.ctime())

        print(colorama.Fore.GREEN, 'backup writed')
    else:
        write_backup(str(int(time.time())), db[0], db[1], time.ctime())
        print(colorama.Fore.GREEN, 'backup writed')


@click.command()
@click.option('--latest', default=False, help='restore latest backup')
@click.option('--oldest', default=False, help='restore oldest backup')
@click.argument('number', default=0)
def restore(latest, oldest, number):

    db = read_db()

    username = input(
        colorama.Fore.YELLOW + 'enter the username : ' + colorama.Fore.LIGHTBLUE_EX
    )

    passwd = input(
        colorama.Fore.LIGHTYELLOW_EX +
        'enter the password for database : ' + colorama.Fore.LIGHTBLUE_EX
    )

    passwd = hash_100(passwd)

    if symmetric_encrypt_str('hi', passwd) == db[1]['auth'][0] and hashlib.sha3_256(username.encode()).hexdigest() in db[0]:
        print(colorama.Fore.GREEN +
              'authentication passed, starting to decrypt password')
        if latest and oldest:
            print(colorama.Fore.RED,
                  'i cant restore latest and oldest backups at once, choose what you need ...')
            return

        if latest:
            backups = [i for i in map(str, sorted(
                [i for i in map(int, os.listdir('./backups'))]))]

            print(colorama.Fore.YELLOW, 'restoring latest backup')

            write_to_db(
                read_backup(backups[0])[0],
                read_backup(backups[0])[1]
            )

            print(colorama.Fore.GREEN, 'backup restored')
        elif oldest:
            backups = [i for i in map(str, sorted(
                [i for i in map(int, os.listdir('./backups'))]))]

            print(colorama.Fore.YELLOW, 'restoring oldest backup')

            write_to_db(
                read_backup(backups[-1])[0],
                read_backup(backups[-1])[1]
            )

            print(colorama.Fore.GREEN, 'backup restored')
        elif len([i for i in map(str, sorted([i for i in map(int, os.listdir('./backups'))]))]) >= number:
            backups = [i for i in map(str, sorted(
                [i for i in map(int, os.listdir('./backups'))]))]

            print(colorama.Fore.YELLOW, 'restoring oldest backup')

            write_to_db(
                read_backup(backups[number])[0],
                read_backup(backups[number])[1]
            )

            print(colorama.Fore.GREEN, 'backup restored')
        else:
            print('incorrect number of backup')
    else:
        print(colorama.Fore.RED + 'authentication failed, try again')


@click.command()
def update():
    os.chdir(
        os.path.abspath('')
    )

    # os.system('git remote add lightning-manager https://github.com/NOTNOTsergey/lightning-manager')

    os.system('git pull lightning-manager main')


@click.command()
def version():
    with open(os.path.join(os.path.abspath(''), 'README.md'), 'r') as file:
        print(colorama.Fore.BLUE, file.readline())


commands.add_command(write)
commands.add_command(read)
commands.add_command(remove)
commands.add_command(list_show)
commands.add_command(version)
commands.add_command(backup)
commands.add_command(update)
commands.add_command(restore)

if __name__ == '__main__':
    commands()
