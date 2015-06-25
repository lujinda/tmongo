#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-25 12:56:22
# Filename      : tmongo.py
# Description   : 
from pymongo.database import Database as db_type, Collection as coll_type
from functools import partial
import time

ROLLBACK_ACTION = ('insert', 'update', 'remove')

class TransactionNotBegin(Exception):
    pass

class TransactionNotEnd(Exception):
    pass

class ActionNotSuport(Exception):
    def __init__(self, action):
        super(ActionNotSuport, self).__init__('%s not suport' % action)

class Transaction():
    queue = []
    def append(self, rollback_func):
        self.queue.append(rollback_func)

    def rollback(self):
        for _func, args in self.queue[::-1]:
            _func(args)
        self.queue = []

class TCollection():
    def __init__(self, collection, tran):
        assert tran != None
        self._collection = collection
        self._tran = tran

    def __getattr__(self, name):
        if name not in dir(self._collection):
            return TCollection(getattr(self._collection, name), self._tran)
        action = name
        if action not in ROLLBACK_ACTION:
            return getattr(self._collection, action)
        exec_func = getattr(self, 'execute_' + action)
        time.sleep(1)
        return exec_func

    def __rollback(self, action, args):
        assert action in ROLLBACK_ACTION
        if not isinstance(args, (list, tuple)):
            args = [args]


        if not args:
            return 

        _rollback = getattr(self, '_rollback_' + action)
        _rollback(args)

    def _rollback_insert(self, args):
        for _id in args:
            self._collection.remove({'_id': _id})

    def _rollback_remove(self, args):
        self._collection.insert(args)

    def _rollback_update(self, args):
        if (not args) or args[0] == None:
            return
        for arg in args:
            self._collection.remove({'_id': arg['_id']})

        self._rollback_remove(args)

    def execute_insert(self, *args, **kwargs):
        result = self._collection.insert(*args, **kwargs)

        self._tran.append((partial(self.__rollback, 'insert'), result))

        return result

    def execute_remove(self, spec_or_id=None, safe=None, multi=True, **kwargs):
        if not isinstance(spec_or_id, dict):
            condition = {'_id': spec_or_id}
        else:
            condition = spec_or_id

        result = self.__get_origin_result(condition, multi)

        self._tran.append((partial(self.__rollback, 'remove'),
                result))

        return self._collection.remove(spec_or_id, safe, multi, **kwargs)

    def execute_update(self, spec, document, upsert=False, manipulate=False, safe=None, multi=False, check_keys=True, **kwargs):
        result = self.__get_origin_result(spec, multi)
        self._tran.append((partial(self.__rollback, 'update'),
                result))

        return self._collection.update(spec, document, upsert , 
                manipulate, safe, multi, check_keys, **kwargs)

    def __get_origin_result(self, condition, multi):
        if multi == False:
            result = self._collection.find_one(condition)
        else:
            result = list(self._collection.find(condition))


        return result

class TMongo(object):
    def __init__(self, db):
        assert isinstance(db, db_type), 'db must pymongo.database.Database'
        self._db = db
        self.tran = None

    def __enter__(self):
        self.begin()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type and exc_value and exc_traceback:
            self.rollback()
        self.end()

    def begin(self):
        if self.tran:
            raise TransactionNotEnd

        self.tran = Transaction()

    def __getattr__(self, name):
        _obj = getattr(self._db, name, None)
        if name in dir(self._db):
            return _obj

        if self.tran != None:
            return TCollection(_obj, self.tran)
        else:
            return _obj

    def __getitem__(self, name):
        return self.__getattr__(name)

    def rollback(self):
        if not self.tran:
            raise TransactionNotBegin
        self.tran.rollback()

    def end(self):
        if not self.tran:
            raise TransactionNotBegin
        self.tran = None

