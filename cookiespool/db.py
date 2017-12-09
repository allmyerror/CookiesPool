# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     db.py
   Description :   redis接口程序
   Author :        Sean
   date：          2017/12/5
-------------------------------------------------
   Change Activity:
                   2017/12/5:
-------------------------------------------------
"""

import random
import redis

from cookiespool.config import *
from cookiespool.error import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password:密码
        """
        if password:
            self._db = redis.Redis(host=host, port=port, password=password)
        else:
            self._db = redis.Redis(host=host, port=port)
        self.domain = REDIS_DOMAIN
        self.name = REDIS_NAME

    def _key(self, key):
        """
        得到格式化的key
        :param key: 最后一个参数
        :return:
        """
        return "{domain}:{name}:{key}".format(domain=self.domain, name=self.name, key=key)

    def set(self, key, value):
        """
        设置键-值对
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    def get(self, key):
        """
        根据键名获取键值
        :param key:
        :return:
        """
        raise NotImplementedError

    def delete(self, key):
        """
        根据键名删除键值对
        :param key:
        :return:
        """
        raise NotImplementedError

    def keys(self):
        """
        得到所有的键名
        :return:
        """
        return self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name))

    def flush(self):
        """
        清空数据库，慎用
        :return:
        """
        self._db.flushdb()


class CookiesRedisClient(RedisClient):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, domain='cookies', name='default'):
        """
        初始化Cookies对象
        :param host: 地址
        :param port: 端口
        :param password:密码
        :param domain: 域，如cookies, account等
        :param name: 名称，一般为站点名，如weibo，默认为default
        """
        RedisClient.__init__(self, host, port, password)
        self.domain = domain
        self.name = name

    def set(self, key, value):
        try:
            self._db.set(self._key(key), value)
        except:
            raise SetCookieError

    def get(self, key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetCookieError

    def delete(self, key):
        try:
            print('Delete', key)
            self._db.delete(self._key(key))
        except:
            raise DeleteCookieError

    def random(self):
        """
        随机取一个cookie
        :param self:
        :return:
        """
        try:
            keys = self.keys()
            return self._db.get(random.choice(keys)).decode('utf-8')
        except:
            raise GetRandomCookieError

    def all(self):
        """
        获取所有cookie，以字典形式返回
        :param self:
        :return:
        """
        try:
            for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username': username,
                        'cookies': self.get(username)
                    }
        except Exception as e:
            print(e.args)
            raise GetAllCookieError

    def count(self):
        """
        获取当前cookies数目
        :param self:
        :return:
        """
        return len(self.keys())


class AccountRedisClient(RedisClient):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, domain='account', name='default'):
        """
        初始化Account对象
        :param host: 地址
        :param port: 端口
        :param password:密码
        :param domain: 域，如cookies, account等
        :param name: 名称，一般为站点名，如weibo，默认为default
        """
        RedisClient.__init__(self, host, port, password)
        self.domain = domain
        self.name = name

    def set(self, key, value):
        try:
            self._db.set(self._key(key), value)
        except:
            raise SetAccountError

    def get(self, key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetAccountError

    def delete(self, key):
        try:
            print('Delete', key)
            self._db.delete(self._key(key))
        except:
            raise DeleteAccountError

    def random(self):
        """
        随机取一个account
        :param self:
        :return:
        """
        try:
            keys = self.keys()
            return self._db.get(random.choice(keys)).decode('utf-8')
        except:
            raise GetRandomAccountError

    def all(self):
        """
        获取所有帐户，以字典形式返回
        :param self:
        :return:
        """
        try:
            for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username': username,
                        'password': self.get(username)
                    }
        except Exception as e:
            print(e.args)
            raise GetAllAccountError

    def count(self):
        """
        获取当前cookies数目
        :param self:
        :return:
        """
        return len(self.keys())


if __name__ == '__main__':
    """
    测试CookiesRedisClient
    conn = CookiesRedisClient(name='weibo')
    conn.set('name1', 'Fike')
    conn.set('name2', 'Sean')
    conn.set('name3', 'Amy')
    conn.get('name')
    conn.get('name2')
    conn.delete('name1')
    conn.set('name1', 'Mike')
    conn.random()
    for a in conn.all():
        print(a)
    conn.count()
    conn.flush()
    
    测试AccountRedisClient
    conn = AccountRedisClient(name='weibo')
    conn.set('18459748505', 'astvar3647')
    conn.set('14760253606', 'gmidy8470')
    conn.set('14760253607', 'uoyuic8427')
    conn.set('18459749258', 'rktfye8937')
    conn.get('18459748505')
    conn.get('14760253606')
    conn.delete('18459748505')
    conn.set('15197170054', 'gmwkms222')
    conn.random()
    for a in conn.all():
        print(a)
    conn.count()
    conn.flush()
    """
