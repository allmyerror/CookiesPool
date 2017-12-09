# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :   开始程序
   Author :        SEAN
   date：          2017/12/9
-------------------------------------------------
   Change Activity:
                   2017/12/9:
-------------------------------------------------
"""

from cookiespool.scheduler import Scheduler


def main():
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()
