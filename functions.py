from random import *
import string
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from getpass import getpass


engine = create_engine('sqlite:///passwords.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    appname = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))



    def __init__(self, appname, username, password):

        self.appname = appname
        self.username = username
        self.password = password


Base.metadata.create_all(engine)


def Generate_key():
    master_password_input = str(getpass("Write your master key and hit ENTER: "))
    master_password = master_password_input.encode()

    #Querying salt
    try :   
        search_object = int(1)
        db = sqlite3.connect('salt_storage.db')
        c = db.cursor()
    
        search_entry = (search_object,)
        query = c.execute('SELECT salt FROM  salts WHERE salt_number = ?;',search_entry)
        for row in query.fetchall():
            salt = row
        salt = salt[0]
    
    except:
        print('Your salt will be create...')
        salt = Generate_salt()
        print('Your salt was saved into the database and is ready now')


    #Generate a key derived from user master password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=300000,


        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password))
    
    master_password = None
    master_password_input = None
    
    return key


def Generate_salt():
    salt = os.urandom(16)
    salt_number = 1
    db = sqlite3.connect('salt_storage.db')
    c = db.cursor()
    entry = (salt_number, salt)
    c.execute('CREATE TABLE IF NOT EXISTS salts (salt_number integer, salt text);')
    c.execute('INSERT INTO salts VALUES (?,?)',entry)
    db.commit()
    db.close()
    return salt


def Show_password():
    search_object = str(input("Write the app name and hit ENTER: "))
    search_object = search_object.lower()
    try:
        account_info = session.query(Account).filter(Account.appname==search_object).first()
        password_saved = account_info.password
        key = Generate_key()
        f = Fernet(key)
        print(f"Your username is: {account_info.username}" '\n')
        print('Your password is: '
        f'\n{f.decrypt(password_saved).decode()}')
    except:
        print('You dont have any saved passwords...')


def Generate_password():

    #Generating a random and strong password
    digits = int(input("How many digits you want in your passsword ? "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(characters) for i in range(digits))
    print(f'Your password is: {password}')
    key = Generate_key()
    

    #Encrypting password using a key derived from user master key
    password = password.encode()
    f = Fernet(key)
    password_encrypted = f.encrypt(password)
    password = None
    
    return password_encrypted


def Store_password(password):

    #Just storing user account data as an object
    app_name = str(input("App name: "))
    app_name = app_name.lower()
    username = str(input("Your username: "))
    insert_account = Account(appname=app_name, username=username, password=password)
    session.add(insert_account)
    session.commit()
    print('Well done, your data was saved!')


def Remove_password():

    #Removing an object from data base
    search_object = str(input("Write the name of the app who you want to remove all data: "))
    remove_data = session.query(Account).filter(Account.appname==search_object).first()
    session.delete(remove_data)
    session.commit()
    print('\n' f'Your {search_object} data was deleted.')

def Clean_data():
    
    #Cleaning all data on database
    print('\n'"This operation will clean up all swordsman data")
    n = int(input(
        '\n[0] Clean up all my passwords and usernames'
        '\n[1] Go back to menu'
        '\n    Choose a number then hit ENTER: '))
    if n == 0:
        session.query(Account).delete()
        session.commit()
        print('\n' '\nAll your acconts informations was deleted')
    if n == 1:
        pass

