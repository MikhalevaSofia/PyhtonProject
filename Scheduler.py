import time
from threading import Thread

import schedule

import calculations
import users
import os
import TelegramBot
import pathlib


def job():
    # for file in os.scandir('./resources/Figure/'):
    #     os.remote(file.path)
    print(f'Clear directory ./resources/Figure/')
    for row in users.users_df.itertuples():
        for tiker in row.tikers.split(','):
            print(calculations.get_calculation(tiker))
            send_pictures_to_users(row.id, tiker)

    print('Finish calculations')


# schedule.every().day.at('10:30').do(job)


schedule.every().seconds.do(job)


def sched():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=sched)
thread.start()


def send_pictures_to_users(id: int, tiker: str):
    for file in os.listdir('./resources/Figure/'):
        if file.startswith(tiker):
            TelegramBot.send_picture(id, pathlib.Path(file).absolute)
