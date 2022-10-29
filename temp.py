from sql import *
import random
import datetime
from time import sleep
from gpiozero import MCP3008

sample_id = 6
vref = 3.3


def fill_samples(user_id):
    while (True):
        sample = sampling(user_id)
        add_sample(sample[0], sample[1], sample[2], sample[3], sample[4])
        print(f"add sample: {sample[0]}|{sample[1]}|{sample[2]}|{sample[3]}|{sample[4]}")
        sleep(0.1)  # sleep 2.4 seconds


def sampling(user_id):
    global sample_id
    sample = [sample_id, user_id, datetime.datetime.now(), round(random.uniform(0, 4.2), 2),
              getVoltage(0)]
    sample_id += 1

    return sample


def getVoltage(channel):
    with MCP3008(channel=channel) as adc:
        return adc.value * vref


fill_samples(1234567)
