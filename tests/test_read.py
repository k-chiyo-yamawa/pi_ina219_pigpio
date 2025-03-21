import sys
import logging
import unittest
from unittest.mock import Mock
from ina219 import INA219
from ina219 import DeviceRangeError


logger = logging.getLogger()
logger.level = logging.ERROR
logger.addHandler(logging.StreamHandler(sys.stdout))


class TestRead(unittest.TestCase):

    GAIN_RANGE_MSG = r"Current out of range \(overflow\)"

    def setUp(self):
        self.ina = INA219(0.1, 0.4)
        self.ina._pi = Mock()
        self.ina._pi.i2c_write_i2c_block_data = Mock()

    def test_read_32v(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0xfa00.to_bytes(2, "big")))
        self.assertEqual(self.ina.voltage(), 32)

    def test_read_16v(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0x7d00.to_bytes(2, "big")))
        self.assertEqual(self.ina.voltage(), 16)

    def test_read_4_808v(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0x2592.to_bytes(2, "big")))
        self.assertEqual(self.ina.voltage(), 4.808)

    def test_read_4mv(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0x8.to_bytes(1, "big")))
        self.assertEqual(self.ina.voltage(), 0.004)

    def test_read_supply_voltage(self):
        self.ina.voltage = Mock(return_value=2.504)
        self.ina.shunt_voltage = Mock(return_value=35.000)
        self.assertEqual(self.ina.supply_voltage(), 2.539)

    def test_read_0v(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'\00'))
        self.assertEqual(self.ina.voltage(), 0)

    def test_read_12ua(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'\01'))
        self.assertAlmostEqual(self.ina.current(), 0.012, 3)

    def test_read_0ma(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'\00'))
        self.assertEqual(self.ina.current(), 0)

    def test_read_negative_ma(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(2, (-0x4d52).to_bytes(2, "big", signed=True)))
        self.assertAlmostEqual(self.ina.current(), -241.4, 1)

    def test_read_0mw(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'\00'))
        self.assertEqual(self.ina.power(), 0)

    def test_read_1914mw(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0x1ea9.to_bytes(2, "big")))
        self.assertAlmostEqual(self.ina.power(), 1914.0, 0)

    def test_read_shunt_20mv(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(2, 0x7d0.to_bytes(2, "big")))
        self.assertEqual(self.ina.shunt_voltage(), 20.0)

    def test_read_shunt_0mv(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'\00'))
        self.assertEqual(self.ina.shunt_voltage(), 0)

    def test_read_shunt_negative_40mv(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.ina._read_voltage_register = Mock(return_value=0xfa0)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(2, (-0xfa0).to_bytes(2, "big", signed=True)))
        self.assertEqual(self.ina.shunt_voltage(), -40.0)

    def test_current_overflow_valid(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_2_80MV)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0xfa1.to_bytes(2, "big")))
        self.assertTrue(self.ina.current_overflow())

    def test_current_overflow_error(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_2_80MV)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0xfa1.to_bytes(2, "big")))
        with self.assertRaisesRegexp(DeviceRangeError, self.GAIN_RANGE_MSG):
            self.ina.current()

    def test_new_read_available(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_2_80MV)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0xA.to_bytes(1, "big")))
        self.assertTrue(self.ina.is_conversion_ready())

    def test_new_read_not_available(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_2_80MV)
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, 0x8.to_bytes(1, "big")))
        self.assertFalse(self.ina.is_conversion_ready())
