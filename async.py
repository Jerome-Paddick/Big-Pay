# from multiprocessing import Process
#
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
#

import asyncio, datetime

async def at_minute_start(cb):
    while True:
        now = datetime.datetime.now()
        after_minute = now.second + now.microsecond / 1_000_000
        if after_minute:
            await asyncio.sleep(60 - after_minute)
        cb()

import time
loop = asyncio.get_event_loop()
loop.create_task(at_minute_start(lambda: print(time.asctime())))
loop.run_forever()