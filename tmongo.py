#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-25 12:56:22
# Filename      : tmongo.py
# Description   : 
from pymongo.database import Database as db_type

class TransactionNotBegin(Exception):
    pass

class TransactionNotEnd(Exception):
    pass

class TMongo(object):
    is_begin = False
    def __init__(self, db):
        assert isinstance(db, db_type), 'db must pymongo.database.Database'
        self._db = db

    def begin(self):
        if self.is_begin:
            raise TransactionNotEnd

        self.is_begin = True

    def __getattr__(self, name):
        return getattr(self._db, name)

    def __setattr__(self, name, value):
        setattr(self._db, name, value)

    def rollback(self):
        if not self.is_begin:
            raise TransactionNotBegin

    def commit(self):
        pass

