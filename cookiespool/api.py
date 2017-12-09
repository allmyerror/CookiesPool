# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     api
   Description :   Flask驱动的API接口
   Author :        SEAN
   date：          2017/12/6
-------------------------------------------------
   Change Activity:
                   2017/12/6:
-------------------------------------------------
"""

from flask import Flask, g

from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    for name in GENERATOR_MAP:
        print(name)
        if not hasattr(g, name):
            setattr(g, name + '_cookies', eval('CookiesRedisClient' + '(name="' + name + '")'))
            setattr(g, name + '_account', eval('AccountRedisClient' + '(name="' + name + '")'))
    return g


@app.route('/<name>/add/<username>/<password>')
def add(name, username, password):
    """
    添加/修改用户， 访问地址如 /weibo/add/user/password 或 /default/add/user/password
    :param name:
    :param username:
    :param password:
    :return:
    """
    g = get_conn()
    getattr(g, name + '_account').set(username, password)
    try:
        getattr(g, name + '_account').get(username)
        return "添加或修改{0}账号'{1}':'{2}'成功".format(name, username, password)
    except:
        return "添加或修改{0}账号'{1}':'{2}'失败".format(name, username, password)


@app.route('/<name>/delete/<username>')
def delete(name, username):
    """
    删除用户， 访问地址如 /weibo/delete/user 或 /default/delete/user
    :param name:
    :param username:
    :return:
    """
    g = get_conn()
    getattr(g, name + '_account').delete(username)
    try:
        getattr(g, name + '_account').get(username)
        return '删除{0}失败'.format(username)
    except:
        return '删除{0}成功'.format(username)


@app.route('/<name>/random')
def random(name):
    """
    获取随机的Cookie，访问地址如 /weibo/random 或 /default/random
    :param name:
    :return: 随机cookie
    """
    g = get_conn()
    cookie = getattr(g, name + '_cookies').random()
    return cookie


@app.route('/<name>/count')
def count(name):
    """
    获取cookies总数
    :param name:
    :return:
    """
    g = get_conn()
    count = getattr(g, name + '_cookies').count()
    return str(count) if isinstance(count, int) else count


if __name__ == '__main__':
    app.run(host='0.0.0.0')
