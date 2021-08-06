version 0.1.1
# LIGHTNING password-manager

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallup.net%2Fwp-content%2Fuploads%2F2019%2F09%2F953236-lightning-storm-rain-clouds-sky-nature-thunderstorm.jpg&f=1&nofb=1)

## - Information

​	The manager encrypts your passwords with symmetric encryption and thus does not give **anyone but you** access to the passwords. Access can be obtained by username and password, which also reduces the chance of someone getting into the database. I want to draw your attention to the fact that **not a single element of the database is stored in the open form**, that is, even if the attackers receive the entire database, it will not give them anything. If you do not need such encryption, then for you there is a password manager without encryption with sqlalchemy base (at the link below). In Lightning manager i used my type of database and its takes up less space then sqlalchemy. 



## links:

| name                  | link                                                         |
| --------------------- | ------------------------------------------------------------ |
| **LIGHTNING manager** | https://github.com/NOTNOTsergey/password-manager/tree/lightning-manager |
| **Password manager**  | https://github.com/NOTNOTsergey/password-manager/ |

## - Installation

```bash
git clone 'the link that you choose'
cd your-directory
./first-launch.sh
```

## - Using LIGHTNING manager

#### First launch

```bash
python cli.py 
```

## - Versions

​		You can find out the version of your manager by entering the command

```bash
python cli.py version
```

The latest version now is 0.1.1

## - Updates
You can update the application in one command:

```bash
./cli.py update 
```
or 
```bash
python cli.py update
```

## - Backups
​	When you use a computer, you can accidentally lose your database. In order not to lose the entire database, you can create backups of the database as you use it. The manager will automatically replace them with new ones if there are more than 5 backups.
command is:

```bash
./cli.py backup
```
You can restore backup in 1 command:

```bash
./cli.py restore [number of the backup in base]
```
To restore latest backup type:
```bash
./cli.py restore --latest
```
To restore oldest backup type:
```bash
./cli.py restore --oldest
```

## - Bugs
​	If you found a bug, write an issue please

# Enjoy...



