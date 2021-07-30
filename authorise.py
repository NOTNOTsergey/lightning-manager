import hashlib
import colorama



def auth():
    '''
    проверяет пароль и если пароля нет то задает
    ВАЖНО: так как в системе используется шифрование юазы данных по паролю то пароль системы не должын совпадать с паролем базы данных
    '''


    password_new = ''
    password_now = ''

    with open('/home/sergey/password-manager/password', 'r') as password_file:
        password_now = password_file.read()
    
    if password_now == '\n' or password_now == '':
        print(colorama.Fore.RED + 'password is not specified')

        colorama.Style.RESET_ALL

        password_new = input(colorama.Fore.YELLOW + 'set the password (you can use the password of any lenght) :')

        colorama.Style.RESET_ALL

        with open('/home/sergey/password-manager/password', 'w') as password_file:
            password_file.write(
                hashlib.sha3_256(password_new.encode()).hexdigest()
            )
        
        print(colorama.Fore.GREEN + 'password succesfully writed')

        
        return None
    else:
        passwd = input(colorama.Fore.YELLOW + 'enter the password: ')

        colorama.Style.RESET_ALL

        if hashlib.sha3_256(passwd.encode()).hexdigest() == password_now:
            print(colorama.Fore.GREEN, 'authentication passed')
            return False
        
        else:
            print(colorama.Fore.RED, 'authectication failed')
            return True
    
def reset_passwd():
    '''
    если нужно стереть существующий пароль то можно воспользоваться этой функцией, если же каким-то образом потерялся пароль от базы данных то это никак не поможет,
    потому что этот пароль НИКАК НЕ ИСПОЛЬЗУЕТСЯ при шифровании базы данных
    '''


    print(colorama.Fore.LIGHTMAGENTA_EX + 'reseting the password')

    colorama.Style.RESET_ALL

    password_new = input(colorama.Fore.YELLOW + 'set the password (you can use the password of any lenght) : ' + colorama.Style.RESET_ALL + colorama.Fore.LIGHTBLUE_EX)

    colorama.Style.RESET_ALL

    with open('/home/sergey/password-manager/password', 'w') as password_file:
        password_file.write(
            hashlib.sha3_256(password_new.encode()).hexdigest()
        )
    
    print(colorama.Fore.GREEN + 'password succesfully writed')
    