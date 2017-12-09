# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     generator.py
   Description :   模拟登录帐号，生成cookies
   Author :        SEAN
   date：          2017/12/6
-------------------------------------------------
   Change Activity:
                   2017/12/6:
-------------------------------------------------
"""

import json

import requests
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pyquery import PyQuery as pq

from cookiespool.config import *
from cookiespool.db import CookiesRedisClient, AccountRedisClient


class CookiesGenerator(object):
    def __init__(self, name='default', browser_type=DEFAULT_BROWSER):
        """
        父类，初始化一些对象
        :param name: 名称
        :param browser_type:浏览器，若不使用浏览器则可设置为 None
        """
        self.name = name
        self.cookies_db = CookiesRedisClient(name=self.name)
        self.account_db = AccountRedisClient(name=self.name)
        self.browser_type = browser_type

    def _init_browser(self, browser_type):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :param browser_type: 浏览器 PhantomJS/ Chrome
        :return:
        """
        if browser_type == 'PhantomJS':
            dcaps = dict(DesiredCapabilities.PHANTOMJS)
            # 设置浏览器头（可以设置从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器）
            dcaps[
                'phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
            # 不载入图片，爬页面速度会快很多
            dcaps["phantomjs.page.settings.loadImages"] = False
            self.browser = webdriver.PhantomJS(desired_capabilities=dcaps)
            self.browser.set_window_size(1366, 768)
        elif browser_type == 'Chrome':
            self.browser = webdriver.Chrome()

    def new_cookies(self, username, password):
        raise NotImplementedError

    def set_cookies(self, account):
        """
        根据账号设置新的cookies
        :param account:
        :return:
        """
        results = self.new_cookies(account.get('username'), account.get('password'))
        if results:
            username, cookies = results
            print('Saving Cookies to Redis', username, cookies)
            self.cookies_db.set(username, cookies)

    def run(self):
        """
        运行，得到所有账号，未生成过cookies账号，生成新cookies
        :return:
        """
        accounts = self.account_db.all()
        cookies = self.cookies_db.all()
        # Account 中对应的用户
        accounts = list(accounts)
        # Cookies 中对应的用户
        userListInCookiesdb = [cookie.get('username') for cookie in cookies]
        print('Getting {0} accounts form Redis'.format(len(accounts)))
        if len(accounts):
            self._init_browser(browser_type=self.browser_type)
        # 不在cookies_db's userlist中的user，需要生成新的cookies
        for account in accounts:
            if not account.get('username') in userListInCookiesdb:
                print('Getting Cookies of ', self.name, account.get('username'), account.get('password'))
                self.set_cookies(account)
        print('Generator Run Finished.')

    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self, name='weibo', browser_type=DEFAULT_BROWSER):
        """
        模拟登陆，产生并存储cookies
        :param name:名称微博
        :param browser_type:使用的浏览器
        """
        CookiesGenerator.__init__(self, name, browser_type)
        self.name = name

    def _success(self, username):
        """
        检查是否能够登录成功
        :param username:
        :return: 新鲜的usernae, cookies键值对
        """
        # 点击submit后，若成功登录后跳转到'http://my.sina.com.cn/profile/logined#location=news'页面
        wait = WebDriverWait(self.browser, 10)
        # 判断搜索按钮是否可以点击
        success = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search_submit'))
        )
        if success:
            print('登录成功')
            # 进一步判断cookies是否有效，即能否正常跳转到'https://weibo.cn/'
            self.browser.get('https://weibo.cn/')

            if '我的首页' in self.browser.title:
                # print(self.browser.get_cookies())
                cookies = {}
                for cookie in self.browser.get_cookies():
                    cookies[cookie['name']] = cookie['value']  # 截取cookie name:value组成键值对，存储起来
                print('成功获取到Cookies')
                print(cookies)
                return (username, json.dumps(cookies))
            elif '解除帐号异常' in self.browser.title:
                print("需要解除异常－通过短信验证码验证身份，删除账号：", username)
                self.account_db.delete(username)
                return None
            else:
                return None

    def download_yzm(self):
        """
        下载验证码图片
        :return:
        """
        wait = WebDriverWait(self.browser, 20)
        try:
            self.browser.find_element_by_css_selector('.loginform_yzm .yzm')
            yzm = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm .yzm')))
            url = yzm.get_attribute('src')
            response = requests.get(url)
            with open('yzm.jpg', 'wb') as f:
                f.write(response.content)
                f.close()
        except NoSuchElementException:
            print("验证码信息有误，重新请求")
            refresh = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.loginform_yzm .reload-code')))
            refresh.click()
            return self.download_yzm()
        except TimeoutException:
            print("无验证码信息，重新请求页面")
            return None

    def manual_verify(self, username, try_count=1):
        """
        手工识别验证码
        :param username:
        :param try_count: 计数器
        :return:
        """
        if try_count > MANUAL_MAX_RETRY:
            print('超过最大重试次数，跳过验证码识别')
            return None
        print('出现验证码，需要手工识别验证码，第{0}次重试'.format(try_count))
        wait = WebDriverWait(self.browser, 20)
        try:
            self.download_yzm()
            inputyzm = input("请打开yzm.jpg，识别后输入验证码，按Enter键确认:\n")
            door = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm input[name="door"]')))
            door.send_keys(inputyzm)
            time.sleep(1)
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.login_btn')))
            submit.click()
            time.sleep(2)
            doc = pq(self.browser.page_source)
            login_error_tips = doc('.layerbox_left .login_error_tips').text()
            if "登录名或密码错误" in login_error_tips:
                print("用户登录名或密码错误，删除用户", username)
                self.account_db.delete(username)
                return None
            elif "验证码" in login_error_tips:
                print("输入的验证码不正确，请重试：")
                return self.manual_verify(username, try_count + 1)
            else:
                return True
        except Exception as e:
            print('验证超时，跳过...', e)
            return None

    def new_cookies(self, username, password):
        """
        生成cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和cookies
        """
        print('Generation Cookies of ', username)
        self.browser.delete_all_cookies()
        self.browser.get('http://my.sina.com.cn/profile/unlogin')
        wait = WebDriverWait(self.browser, 20)

        try:
            login = wait.until(EC.visibility_of_element_located((By.ID, 'hd_login')))
            login.click()
            user = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="loginname"]')))
            user.send_keys(username)
            psd = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="password"]')))
            psd.send_keys(password)
            time.sleep(1)
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.login_btn')))
            submit.click()
            try:
                result = self._success(username)
                if result:
                    return result
            except TimeoutException:
                if self.manual_verify(username):
                    result = self._success(username)
                    if result:
                        return result
        except Exception as e:
            print('未知异常，跳过...', e)


if __name__ == '__main__':
    generator = WeiboCookiesGenerator()
    generator._init_browser('Chrome')
    generator.new_cookies('14760253606', 'gmidy8470')
