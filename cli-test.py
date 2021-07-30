import db_api
from os import sys
import os
from db_api.table import Password

db_api.global_init(db_api.sqlite_format_string('/home/sergey/password-manager/db/db.sqlite3'))

