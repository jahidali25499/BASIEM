import time
from apscheduler.schedulers.background import BackgroundScheduler


def alert_1():

    print("Alert 1 Started")
    print("Alert 1 Finished")


def alert_2():
    
    print("Alert 2 Started")
    print("Alert 2 Finished")


def alert_3():
    print("Alert 3 Started")
    print("Alert 3 Finished")


try:
    
    scheduler = BackgroundScheduler()

    scheduler.add_job(alert_1, 'interval', seconds=10)
    scheduler.add_job(alert_2, 'interval', seconds=5)
    scheduler.add_job(alert_3, 'interval', seconds=2)

    scheduler.start()

except KeyboardInterrupt:
    time.sleep(5)
    scheduler.shutdown()
