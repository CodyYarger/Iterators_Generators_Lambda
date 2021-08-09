#!/usr/bin/env python3
# 05/24/2021
# Dev: Cody Yarger
# Assignment 04 - Iterables, Iterators & Generators

'''
    Provides a basic frontend
'''
# pylint: disable=C0103
# pylint: disable=W0106
import sys
from datetime import datetime
#import pysnooper
from loguru import logger
import main
import socialnetwork_model as sn

log_file = datetime.now().strftime("log_%m_%d_%Y.log")
logger.add(log_file, level="INFO")


# @pysnooper.snoop()
def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    if main.load_users(filename):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


# @pysnooper.snoop()
def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    if main.load_status_updates(filename):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


# @pysnooper.snoop()
def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')

    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection
                         ):
        print("Error occurred while trying to add new user")
    else:
        print("User was successfully added")


# @pysnooper.snoop()
def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')

    if not main.update_user(user_id,
                            email,
                            user_name,
                            user_last_name,
                            user_collection
                            ):
        print("Error occurred while trying to update user")
    else:
        print("User was successfully updated")


# @pysnooper.snoop()
def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')

    try:
        result = main.search_user(user_id, user_collection)
        print(f'User id: {result.user_id}')
        print(f'User name: {result.user_name}')
        print(f'User last name: {result.user_last_name}')
        print(f'User email: {result.user_email}')
    except AttributeError:
        print("Error: User does not exist")


# @pysnooper.snoop()
def delete_user():
    '''
        Deletes user from the database
    '''
    user_id = input('User ID: ')

    if not main.delete_user(user_id, user_collection):
        print("Error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


# @pysnooper.snoop()
def add_status():
    '''
        Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("Error occurred while trying to add new status")
    else:
        print("New status was successfully added")


# @pysnooper.snoop()
def update_status():
    '''
        Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id,
                              user_id,
                              status_text,
                              status_collection
                              ):
        print("Error occurred while trying to update status")
    else:
        print("Status was successfully updated")


# @pysnooper.snoop()
def search_status():
    '''
        Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    try:
        result = main.search_status(status_id, status_collection)
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")
    except AttributeError:
        print("Error: Status ID does not exist")


# @pysnooper.snoop()
def delete_status():
    '''
        Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("Error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


# @pysnooper.snoop()
def search_all_status_updates():
    '''
        Deletes status from the database
    '''
    user_id = input("Enter User ID: ")

    # query database for all status_text objects associated to user_id
    status_query = main.search_all_status_updates(user_id, status_collection)
    total = len(status_query)
    print(f'{total} status updates were located for {user_id}')

    # call status_generator and step through generator yeild objects
    generator = status_generator(status_query)
    while True:
        selection = input('Enter Y/N to see next update: ')
        if selection.lower() == "y":
            try:
                next(generator)
            except StopIteration:
                print("End of query list reached")
                break
        elif selection.lower() == "n":
            break


# @pysnooper.snoop()
def status_generator(query):
    '''
        Generator function for status text
    '''
    x = 0
    for text in query:
        yield print(text.status_text)
        x += 1


def filter_status_by_string():
    '''
        Returns status text that meets search criteria
    '''
    search_string = input('Enter search string: ')
    try:
        query = main.filter_status_by_string(search_string, status_collection)
    except AttributeError:
        # return print('Error calling function')
        print('Error calling function')
    while True:
        # prompt user to step through query
        selection = input('Enter Y/N to see next update: ')
        if selection.lower() == "y":
            try:
                next_result = next(query)
                print(f'User ID {next_result.user_id}: {next_result.status_text}')
            except StopIteration:
                print("End of query reached")
                break

            # prompt user to delete status_text
            delete_yn = input('Delete this status? Y/N: ')
            if delete_yn.lower() == "y":
                try:
                    next_result.delete_instance()
                    print('Status text deleted successfully')
                except NameError:
                    print('Error deleting status text')
            else:
                continue
        elif selection.lower() == "n":
            break


def flagged_status_updates():
    '''
        Prints collection of status text that meets search criteria
    '''
    search_string = input('Enter search string: ')
    try:
        query = main.filter_status_by_string(search_string, status_collection)
    except AttributeError:
        print('Error calling function')
    [print((query.user_id.user_id, query.status_text)) for query in query]


def quit_program():
    '''
        Quits program
    '''
    print("Exiting program")
    sn.db.close()
    sys.exit()


if __name__ == '__main__':

    # instantiate database
    data_b = sn.db
    data_b.connect()
    data_b.execute_sql('PRAGMA foreign_keys = ON;')

    # instantiate user and user_collection
    user_collection = main.init_user_collection(data_b)
    status_collection = main.init_status_collection(data_b)

    # user menu
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': search_all_status_updates,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': filter_status_by_string,
        'M': flagged_status_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Search all status updates
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Search all status updates matching a string
                            M: Show all flagged status updates
                            Q: Quit

                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
