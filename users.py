#!/usr/bin/env python3
# 05/24/2021
# Dev: Cody Yarger
# Assignment 04 - Iterables, Iterators & Generators
'''
    User Classes for social network project
'''
# pylint: disable=E1101
# pylint: disable=R0201

from loguru import logger
#import pysnooper
import peewee as pw
from socialnetwork_model import UsersTable


class UserCollection():
    '''
        Contains a database of Users Model Instances
    '''

    def __init__(self, database):
        self.database = database
        logger.info("New UserCollection instantiated")

    # @pysnooper.snoop()
    def add_user(self, user_id, email, user_name, user_last_name):
        '''
            Adds a new user to user collection
        '''
        with self.database.transaction():
            try:
                new_user = UsersTable.create(
                    user_id=user_id,
                    user_name=user_name,
                    user_last_name=user_last_name,
                    user_email=email
                )
                new_user.save()
                logger.info(f'user_id {user_id} added to database')
                return True
            except pw.IntegrityError:
                logger.info(f'user_id {user_id} in database of len user_id > 30')
                return False

    # @pysnooper.snoop()
    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
            Modifies an existing Model Instance
        '''
        try:
            query = UsersTable.get_by_id(user_id)
            query.user_name = user_name
            query.user_last_name = user_last_name
            query.user_email = email
            query.save()
            logger.info(f'user_id {user_id} modified')
            return True
        except UsersTable.DoesNotExist:
            logger.info(f'No user_id {user_id} in the database')
            return False

    # @pysnooper.snoop()
    def delete_user(self, user_id):
        '''
            Deletes an existing Model Instance
        '''
        try:
            query = UsersTable.get_by_id(user_id)
            query.delete_instance()
            logger.info(f'user_id import pysnooper{user_id} deleted')
            return True
        except UsersTable.DoesNotExist:
            logger.info(f'No user_id {user_id} in the database')
            return False

    # @pysnooper.snoop()
    def search_user(self, user_id):
        '''
            Searches for existing Model Instance
        '''
        try:
            query = UsersTable.get_by_id(user_id)
            logger.info(f'user_id {user_id} found')
            return query
        except UsersTable.DoesNotExist:
            logger.info(f'No user_id {user_id} in the database')
            return False
