# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     error.py
   Description :   报错信息
   Author :        SEAN
   date：          2017/12/5
-------------------------------------------------
   Change Activity:
                   2017/12/5:
-------------------------------------------------
"""


class CookiePoolError(Exception):
    def __str__(self):
        return repr("Cookie Pool Error")


class SetCookieError(CookiePoolError):
    def __str__(self):
        return repr("Set Cookie Error")


class GetCookieError(CookiePoolError):
    def __str__(self):
        return repr("Get Cookie Error")


class DeleteCookieError(CookiePoolError):
    def __str__(self):
        return repr("Delete Cookie Error")


class GetRandomCookieError(CookiePoolError):
    def __str__(self):
        return repr("Get Random Cooke Error")


class GetAllCookieError(CookiePoolError):
    def __str__(self):
        return repr("Get All Cookie Error")


class SetAccountError(CookiePoolError):
    def __str__(self):
        return repr("Set Accout Error")


class GetAccountError(CookiePoolError):
    def __str__(self):
        return repr('Get Account Error')


class DeleteAccountError(CookiePoolError):
    def __str__(self):
        return repr('Delete Account Error')


class GetRandomAccountError(CookiePoolError):
    def __str__(self):
        return repr("Get Random Account Error")


class GetAllAccountError(CookiePoolError):
    def __str__(self):
        return repr('Get All Account Error')
