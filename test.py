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
    db.begin()
    try:
        db.account.insert({'uid': 100})
        raise Exception
    except Exception as e:
        db.rollback()
    finally:
        db.commit()

    print(list(db.account.find()))

if __name__ == "__main__":
    main()

