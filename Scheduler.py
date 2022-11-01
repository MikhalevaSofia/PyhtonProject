import time

import schedule

import calculations


def job(user_tikers: str):
    for tiker in user_tikers.split(','):
        print(calculations.get_calculation(tiker))


schedule.every().day.at('10:30', 'Europe/Moscow').do(job)


def sched():
    while True:
        schedule.run_pending()
        time.sleep(1)


t = Thread(target=sched)
t.start
while True:
    schedule.run_pending()
    time.sleep(1)
