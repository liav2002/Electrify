from sql import *
import random
import datetime
import time

id = 6


def fill_samples():
    while (True):
        sample = sampling(12345677)
        add_sample(sample[0], sample[1], sample[2], sample[3], sample[4])
        print(f"add sample: {sample[0]}|{sample[1]}|{sample[2]}|{sample[3]}|{sample[4]}")
        time.sleep(2.4)  # sleep 2.4 seconds


def sampling(user_id):
    global id
    sample = [id, user_id, datetime.datetime.now(), round(random.uniform(0, 4.2), 2),
              round(random.uniform(0, 100.0), 2)]
    id += 1

    return sample


fill_samples()
