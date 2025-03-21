#!/usr/bin/env python

import time
import logging
from ina219 import INA219

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

READS = 100




def init(ina):
    ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)


def read(ina):
    for x in range(0, READS):
        ina.voltage()


if __name__ == "__main__":
    with INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO) as ina:
        init(ina)
        start = time.time()
        read(ina)
        finish = time.time()
        elapsed = (finish - start) * 1000000
        print("Read time (average over %d reads): %d microseconds" %
              (READS, int(elapsed / READS)))
