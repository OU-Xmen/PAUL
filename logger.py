import datetime as dt
import os

timestamp = dt.datetime.now()
date = timestamp.date()



def log(message = None, Type = 1):
    if Type == 1:
        Type = "INFO"
    elif Type == 2:
        Type = "ERROR"
    elif Type == 3:
        Type = "WARNING"
    elif Type == 4:
        Type = "CRITICAL"
    f = open(f"logs/PAUL {date}.log", "a")
    f.write(f"[{Type}] [{timestamp}] {message}\n")
    f.close()