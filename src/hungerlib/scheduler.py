# HungerLib's simple snap scheduler
import time
from datetime import datetime, timedelta


def snapSchedule(logger, minimumMinutes=30, snapMinutes=(0, 30)):

    now = datetime.now()
    logger.info(f"Current time: {now.strftime('%I:%M:%S %p')}")
    minimum = now + timedelta(minutes=minimumMinutes)
    logger.info(f"Minimum threshold: {minimum.strftime('%I:%M:%S %p')}")
    snapMinutes = sorted(snapMinutes)
    for snap in snapMinutes:
        if minimum.minute < snap:
            scheduled = minimum.replace(minute=snap, second=0, microsecond=0)
            break
    else:
        scheduled = (minimum.replace(minute=0, second=0, microsecond=0)
                     + timedelta(hours=1))
    formatted = scheduled.strftime("%I:%M %p")
    logger.warn(f"Scheduled for <aqua>{formatted}<reset>.")
    logger.info(f"Scheduled datetime object: {scheduled}")
    return scheduled
    

def secsUntil(target):
    now = datetime.now()
    return int((target - now).total_seconds())

def minsUntil(target):
    now = datetime.now()
    return int((target - now).total_seconds()) // 60