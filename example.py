#!/usr/bin/env python

import logging

from ina219 import INA219

SHUNT_OHMS = 0.01
MAX_EXPECTED_AMPS = 5.0


def read():
    with INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO) as ina:
        ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

        print("Bus Voltage    : %.3f V" % ina.voltage())
        print("Bus Current    : %.3f mA" % ina.current())
        print("Supply Voltage : %.3f V" % ina.supply_voltage())
        print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
        print("Power          : %.3f mW" % ina.power())


if __name__ == "__main__":
    read()
