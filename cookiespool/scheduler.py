# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     scheduler
   Description :   调度程序
   Author :        SEAN
   date：          2017/12/9
-------------------------------------------------
   Change Activity:
                   2017/12/9:
-------------------------------------------------
"""

import time
from multiprocessing import Process

from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Checking Cookies')
            try:
                for name, cls in TESTER_MAP.items():
                    tester = eval(cls + '(name="' + name + '")')
                    tester.run()
                    print('Tester Finished')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Generating Cookes')
            try:
                for name, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(name="' + name + '")')
                    generator.run()
                    print('Generator Finished')
                    generator.close()
                    print('Deleted Generator')
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        if GENERATOR_PROCESS:
            generator_process = Process(target=Scheduler.generate_cookie())
            generator_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie())
            valid_process.start()

        if API_PROCESS:
            api_process = Process(target=Scheduler.api())
            api_process.start()


if __name__ == '__main__':
    s = Scheduler()
    s.run()
