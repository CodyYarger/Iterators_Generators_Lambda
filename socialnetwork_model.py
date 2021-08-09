#!/usr/bin/env python3
# 05/24/2021
# Dev: Cody Yarger
# Assignment 04 - Iterables, Iterators & Generators
''' Database interface '''

# pylint: disable=C0103
# pylint: disable=R0903

import os
import peewee as pw

file = 'socialnetwork.db'
path = os.getcwd()
if os.path.exists(file):
    os.remove(file)
#db = pw.SqliteDatabase(file)
db = pw.SqliteDatabase(':memory:')


class BaseModel(pw.Model):
    """ Base Model """

    class Meta:
        ''' Meta class '''
        database = db


class UsersTable(BaseModel):
    """
        This class defines users model, with fields:
        user_id, user_name, user_last_name, and user_email.
    """
    user_id = pw.CharField(primary_key=True,
                           constraints=[pw.Check("LENGTH(user_id) <= 30")])
    user_name = pw.CharField(constraints=[pw.Check("LENGTH(user_name) <= 30")])
    user_last_name = pw.CharField(
        constraints=[
            pw.Check("LENGTH(user_last_name) <= 100")
        ])
    user_email = pw.CharField()


class StatusTable(BaseModel):
    """
        This class defines a users status model, with fields:
        status_id, user_id, and status_text.
    """
    user_id = pw.ForeignKeyField(UsersTable,
                                 on_delete="CASCADE")
    status_id = pw.CharField(primary_key=True)
    status_text = pw.CharField()
