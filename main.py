from random import *
import string
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
import functions
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


print('\n' '\n' '       Welcome to swordsman :)')
n = None
while n != 0:
    n = int(input(
        '\n' '\n'
        '\n       Choose a number and hit ENTER:''\n'
        '\n[0] -> Exit swordsman'
        '\n[1] -> Generate a new password'
        '\n[2] -> Query your password'
        '\n[3] -> Remove password information'
        '\n[4] -> Clean all data''\n    -> '
        
    ))
    if n == 1:
        password = functions.Generate_password()
        functions.Store_password(password)
    if n == 2:
        functions.Show_password()
    if n == 3:
        functions.Remove_password()
    if n == 4:
        functions.Clean_data()
   
