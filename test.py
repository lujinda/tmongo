#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-25 12:56:36
# Filename      : test.py
# Description   : 
from tmongo import TMongo
from pymongo import Connection

def main():
    db = Connection().test
    db = TMongo(db)
    print('begin', list(db.account.find()))
    try:
        with db:
            db.account.insert({'uid': 1})
            db.account.insert({'uid': 2})
            db.account.update({'uid': 444}, {'$set': {'uid': 666}})
            raise Exception
    except Exception as e:
        print(e)

    print('after', list(db.account.find()))


if __name__ == "__main__":
    main()

