from DAL.SQL.sql import *
import datetime
from time import sleep
from ina219 import INA219
from random import uniform

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
ADDRESS = 0x40


class INA219Handler:
    def __init__(self, address=ADDRESS, shunt_ohms=SHUNT_OHMS, max_expected_amps=MAX_EXPECTED_AMPS):
        self.ina = INA219(shunt_ohms=shunt_ohms, max_expected_amps=max_expected_amps, address=address)
        self.ina.configure()

    def getVoltage(self):
        return self.ina.voltage()

    def getCurrent(self):
        return self.ina.current()

    def getPower(self):
        return self.ina.power()


def fill_samples(user_id):
    sample_id = get_number_of_samples(user_id)  # starting id from zero. next id equal to number of samples.
    # ina_handler = INA219Handler()

    try:
        while True:
            # Generate sample
            """sample = [sample_id, user_id, datetime.datetime.now(), round(ina_handler.getPower(), 3),
                      round(ina_handler.getVoltage(), 3)]"""

            powerValue = 0.09
            voltageValue = 0.33

            deltaPower = -0.003 + uniform(0.001, 0.003)
            deltaVoltage = -0.003 + uniform(0.005, 0.01)

            sample = [sample_id, user_id, datetime.datetime.now(), round(powerValue + deltaPower, 3),
                      round(voltageValue + deltaVoltage, 3)]

            # Insert sample to DB
            if add_sample(sample[0], sample[1], sample[2], sample[3], sample[4]):
                print(f"add sample: {sample[0]}|{sample[1]}|{sample[2]}|{sample[3]}|{sample[4]}")

                # Increment sample id
                sample_id += 1

            else:
                print("add sample failed.")

            # Sleep for 1 second
            sleep(1)

    except Exception as e:
        print("ERROR:fill_samples: " + str(e))


fill_samples(12345677)
