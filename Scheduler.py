import time
from threading import Thread

import schedule

import calculations
import users


def job():
    for row in users.users_df.itertuples():
        for tiker in user_tikers.split(','):
            print(calculations.get_calculation(tiker))


schedule.every().day.at('10:30', 'Europe/Moscow').do(job)


def sched():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=sched)
thread.start()
