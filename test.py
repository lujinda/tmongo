#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-25 12:56:36
# Filename      : test.py
# Description   : 
from tmongo import TMongo
from pymongo import Connection
from multiprocessing import Process

def main():
    db = Connection().test
    db = TMongo(db)
    db.account.update({'user': 'a1'}, {'user': 'a1', 'balance': 1000}, upsert = True)
    db.account.update({'user': 'a2'}, {'user': 'a2', 'balance': 1000}, upsert = True)
    print('before', list(db.account.find()))
    try:
        with db:
            db.account.update({'user': 'a1'}, {"$inc": {'balance': -500}})
            db.account.update({'user': 'a2'}, {"$inc": {'balance': 500}})
            raise Exception
    except Exception as e:
        print(e)

    print('after', list(db.account.find()))


if __name__ == "__main__":
    main()

