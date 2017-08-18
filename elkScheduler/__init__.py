from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from logger import logger


class elkCron():
    def mailScheduler(func, config, q):
        sched = BackgroundScheduler()
        for event in config:
            sched.add_job(func, 'cron', [event, q],
                          id=event['name'],
                          year=event["schedule"]["year"],
                          month=event["schedule"]["month"],
                          day=event["schedule"]["day"],
                          minute=event["schedule"]["minute"],
                          second=event["schedule"]["second"]
                          )
        return(sched)

    def elkDefaulFunc(event, q):
        now = datetime.today()
        try:
            event['start_time'] = event['end_time']
            event['end_time'] = now
        except KeyError:
            event['start_time'] = now.replace(hour=0, minute=0, second=0, microsecond=0)
            event['end_time'] = now
        q.put(event)
        logger.debug("Put message to queue, event['name'] = " + event['name'])
#        #print(q.qsize())


# def job_function():
#     print("Hello World")
# def job_function1():
#     print("Hi1")
# sched = BlockingScheduler()
# # Schedules job_function to be run on the third Friday
# # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
# sched.add_job(job_function, 'cron', id='New1', month='*', day='*', hour='*', minute='*', second='*')
# sched.add_job(job_function1, 'cron', id='New1', month='*', day='*', hour='*', minute='*', second='*/3')
# print(sched.get_jobs())
# sched.start()
