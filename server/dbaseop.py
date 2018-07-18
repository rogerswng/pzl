# -*- coding: utf-8 -*-

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

class Pysql(object):
    """
    Database Connection Class Encapsulation
    Based on PyMySQL(like pyodbc)
    """

    # Database connection pool Object
    __pool = None

    def __init__(self):
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        if Pysql.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                mincached=1,
                maxcached=20,
                host="127.0.0.1",
                port=3306,
                user="root",
                password="rootroot",
                # db -- database name, 按需修改
                db="pzl",
                charset="utf8",
                cursorclass=DictCursor
            )

        return __pool.connection()

    def close(self):
        """
        close connection
        """
        self._conn.close()

    def query(self, sql, params=None):
        if params is None:
            return self._cursor.execute(sql)
        else:
            return self._cursor.execute(sql, params)

    def selectAll(self, sql, params=None):
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count >= 0:
            return {"success":True,"count":count,"data":self._cursor.fetchall()}
        else:
            return {"success":False}

    def selectFirst(self, sql, params=None):
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count >= 0:
            return {"success":True,"count":count,"data":self._cursor.fetchone()}
        else:
            return {"success":False}

    def selectSome(self, sql, num, params=None):
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count >= 0:
            return {"success":True,"count":count,"data":self._cursor.fetchmany(num)}
        else:
            return {"success":False}

    def insert(self, sql, params):
        count = self._cursor.execute(sql, params)
        if count:
            self._conn.commit()
            return {"success":True}
        else:
            return {"success":False}

    def delete(self, sql, params=None):
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count >= 0:
            self._conn.commit()
            return {"success":True,"count":count}
        else:
            return {"success":False,"reason":1}

    def modify(self, sql, params=None):
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count >= 0:
            self._conn.commit()
            return {"success":True,"count":count}
        else:
            return {"success":False}
