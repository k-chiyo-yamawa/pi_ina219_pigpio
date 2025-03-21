import sys
import logging
import unittest
from unittest.mock import Mock, call
from ina219 import INA219
from ina219 import DeviceRangeError

logger = logging.getLogger()
logger.level = logging.ERROR
logger.addHandler(logging.StreamHandler(sys.stdout))

HANDLE = 567

class TestReadAutoGain(unittest.TestCase):

    GAIN_RANGE_MSG = r"Current out of range \(overflow\)"

    def test_auto_gain(self):
        self.ina = INA219(0.1, 0.4)
        self.ina._pi = Mock()
        self.ina._pi.i2c_write_i2c_block_data = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)

        self.ina._read_voltage_register = Mock()
        self.ina._read_voltage_register.side_effect = [0xfa1, 0xfa0]
        self.ina._read_configuration = Mock()
        self.ina._read_configuration.side_effect = [0x99f, 0x99f]
        self.ina._current_register = Mock(return_value=100)

        self.assertAlmostEqual(self.ina.current(), 4.878, 3)

        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x09, 0x9f]),
                 call(HANDLE, 0x05, [0x20, 0xcc]), call(HANDLE, 0x00, [0x11, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_auto_gain_out_of_range(self):
        self.ina = INA219(0.1, 3.0)
        self.ina._pi = Mock()
        self.ina._pi.i2c_write_i2c_block_data = Mock()
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)

        self.ina._read_voltage_register = Mock(return_value=0xfa1)
        self.ina._read_configuration = Mock(return_value=0x199f)

        with self.assertRaisesRegexp(DeviceRangeError, self.GAIN_RANGE_MSG):
            self.ina.current()
