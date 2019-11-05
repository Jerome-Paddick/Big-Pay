import datetime
import asyncio

async def at_minute_start(cb):
    now = datetime.datetime.now()
    wait_for_next_minute = False
    while True:
        after_minute = now.second + now.microsecond / 1_000_000
        if after_minute != 0:
            to_next_minute = 60 - after_minute
        else:
            to_next_minute = 0  # already at the minute start
        if wait_for_next_minute:
            to_next_minute += 60
        await asyncio.sleep(to_next_minute)
        cb()
        prev = now
        now = datetime.datetime.now()
        # if we're still at the same minute, our sleep was slightly
        # too short, so we'll need to wait an additional minute
        wait_for_next_minute = now.minute == prev.minute