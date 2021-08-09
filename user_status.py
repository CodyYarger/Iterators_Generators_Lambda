#!/usr/bin/env python3
# 05/24/2021
# Dev: Cody Yarger
# Assignment 04 - Iterables, Iterators & Generators
'''
    User status Classes for social network project
'''

from loguru import logger
import peewee as pw
from socialnetwork_model import StatusTable
#import pysnooper

# pylint: disable=E1101
# pylint: disable=R0201


class UserStatusCollection():
    '''
        Contains a collection of User Status objects
    '''

    def __init__(self, database):
        self.database = database
        logger.info('New UserStatusCollection instantiated')

    # @pysnooper.snoop()
    def add_status(self, user_id, status_id, status_text):
        '''
            Adds new status to user status collection
        '''

        with self.database.transaction():
            try:
                new_status = StatusTable.create(
                    user_id=user_id,
                    status_id=status_id,
                    status_text=status_text
                )
                new_status.save()
                logger.info(f'user_id {user_id} status added to database')
                return True
            except pw.IntegrityError:
                logger.info(f'user_id {user_id} already in database')
                return False

    def modify_status(self, status_id, user_id, status_text):
        '''
            Modifies user status
        '''
        try:
            StatusTable.get(user_id=user_id)
            query = StatusTable.get_by_id(status_id)
            query.status_text = status_text
            query.save()
            logger.info(f'status: {status_id} text updated')
            return True

        except StatusTable.DoesNotExist:
            logger.info(f'No status_id {status_id} in the database')
            return False

    # @pysnooper.snoop()pass
    def delete_status(self, status_id):
        '''
            Deletes user status
        '''
        try:
            query = StatusTable.get_by_id(status_id)
            query.delete_instance()
            logger.info(f'status_id {status_id} deleted')
            return True
        except StatusTable.DoesNotExist:
            logger.info(f'No status_id {status_id} in the database')
            return False

    # @pysnooper.snoop()
    def search_status(self, status_id):
        '''
            Searches for user status
        '''
        try:
            query = StatusTable.get_by_id(status_id)
            logger.info(f'status_id {status_id} found')
            return query

        except StatusTable.DoesNotExist:
            logger.info(f'No status_id {status_id} in the database')
            return False

    # @pysnooper.snoop()
    def search_all_status_updates(self, user_id):
        '''
            Takes a user id and retuns all status updates
        '''
        try:
            query = StatusTable.select().where(StatusTable.user_id == user_id)
            return query
        except StatusTable.DoesNotExist:
            logger.info(f'No User ID {user_id} in the database')
            return False

    def filter_status_by_string(self, search_string):
        '''
            Returns iterator of status_id's containing search_string
        '''
        query = StatusTable.select().where(
            StatusTable.status_text.contains(search_string)).iterator()
        return query
