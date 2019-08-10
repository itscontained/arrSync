#!/usr/bin/env python3
from time import sleep
from os import environ as env
from apscheduler.schedulers.background import BackgroundScheduler

from arrSync import run

cron = env.get('ARRSYNC_CRON_SCHEDULE', '*/15 * * * *').split()
if len(cron) != 5:
    exit('Cron expression configured incorrectly')

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    run,
    name=f'arrSync',
    trigger='cron',
    minute=cron[0],
    hour=cron[1],
    day=cron[2],
    month=cron[3],
    day_of_week=cron[4],
    misfire_grace_time=15
)

while scheduler.get_jobs():
    sleep(1)

scheduler.shutdown()
