#!/usr/bin/env python3
# 05/24/2021
# Dev: Cody Yarger
# Assignment 04 - Iterables, Iterators & Generators

''' Main for enstantiating Users, UsersCollecton, UserStatus and
UserStatusCollection. Users and UserStatus objects can be defined and
collected in UserCollection and UserStatusCollection database objects. '''
# pylint: disable=C0103
# pylint: disable=R0903

import os
import csv
from loguru import logger
import peewee as pw
import user_status
import users
import socialnetwork_model as sn


def init_user_collection(database):
    '''
        Creates and returns a new instance of UserCollection
    '''
    database.create_tables([sn.UsersTable])
    return users.UserCollection(database)


def init_status_collection(database):
    '''
        Creates and returns a new instance of UserStatusCollection
    '''
    database.create_tables([sn.StatusTable])
    return user_status.UserStatusCollection(database)


def load_users(filename):
    '''
        Opens a CSV file with user data and loads it to a SQL database.
        Requirements:
        - If a user_id already exists, it will ignore it and continue to the next.
        - Returns False if there are any errors (such as empty fields in the source
         CSV file)
        - Otherwise, it returns True.
    '''
    cwd = os.getcwd()

    try:
        with open((cwd + "/" + filename + ".csv"), newline='') as accounts_csv:
            reader = csv.DictReader(accounts_csv)
            for row in reader:
                for _, dvalue in row.items():
                    if dvalue == '':
                        logger.info("Error in CSV file")
                        return False
                try:
                    with sn.db.transaction():
                        new_user = sn.UsersTable.create(
                            user_id=row['USER_ID'],
                            user_name=row['NAME'],
                            user_last_name=row['LASTNAME'],
                            user_email=row['EMAIL']
                        )
                        new_user.save()
                except pw.IntegrityError:
                    return False
            return True
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False


def load_status_updates(filename):
    '''
        Opens a CSV file with status data and adds it to an existing instance of
        UserStatusCollection

        Requirements:
        - If a status_id already exists, it will ignore it
         and continue to the next.
        - Returns False if there are any errors (such as empty fields in the
         source CSV file)
        - Otherwise, it returns True.
    '''
    cwd = os.getcwd()

    try:
        with open((cwd + "/" + filename + ".csv"), newline='') as status_csv:
            reader = csv.DictReader(status_csv)
            for row in reader:
                for __, dvalue in row.items():
                    if dvalue == '':
                        logger.info("Error in CSV file")
                        return False
                try:
                    with sn.db.transaction():
                        sn.new_status = sn.StatusTable.create(
                            status_id=row['STATUS_ID'],
                            user_id=row['USER_ID'],
                            status_text=row['STATUS_TEXT']
                        )
                        sn.new_status.save()
                except pw.IntegrityError:
                    return False
            return True
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if user_collection.
    add_user() returns False).
    - Otherwise, it returns True.
    '''
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    return user_collection.modify_user(user_id,
                                       email,
                                       user_name,
                                       user_last_name
                                       )


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    return user_collection.search_user(user_id)


def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    return status_collection.add_status(user_id, status_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    return status_collection.search_status(status_id)


def search_all_status_updates(user_id, status_collection):
    ''' takes a user id and retuns all status updates '''
    return status_collection.search_all_status_updates(user_id)


def filter_status_by_string(search_string, status_collection):
    ''' takes a user search criteria and returns associated status_text '''
    return status_collection.filter_status_by_string(search_string)
