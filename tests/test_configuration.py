import sys
import logging
import unittest
from unittest.mock import Mock, call
from ina219 import INA219

logger = logging.getLogger()
logger.level = logging.ERROR
logger.addHandler(logging.StreamHandler(sys.stdout))

HANDLE = 1234

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.ina = INA219(0.1, 0.4)
        self.ina._pi = Mock(name="_pi")
        self.ina._pi.i2c_write_i2c_block_data = Mock(name="i2c_write_i2c_block_data", return_value=(2, b'ab'))

        self.ina._i2c_handle = HANDLE

    def test_calibration_register_maximum_is_fffe_1_ohm(self):
        self.ina = INA219(1.0, 0.01)
        self.ina._pi = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        calls = [call(HANDLE, 0x05, [0xFF, 0xFE]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_calibration_register_maximum_is_fffe_100_mohm(self):
        self.ina = INA219(0.1, 0.1)
        self.ina._pi = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        calls = [call(HANDLE, 0x05, [0xFF, 0xFE]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_calibration_register_maximum_is_fffe_10_mohm(self):
        self.ina = INA219(0.01, 0.1)
        self.ina._pi = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        calls = [call(HANDLE, 0x05, [0xFF, 0xFE]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_auto_gain_with_expected_amps(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)
        self.assertEqual(self.ina._gain, 1)
        self.assertEqual(self.ina._voltage_range, 0)
        self.assertTrue(self.ina._auto_gain_enabled)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x09, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_auto_gain_no_expected_amps(self):
        self.ina = INA219(0.1)
        self.ina._pi = Mock()
        self.ina._pi.i2c_write_i2c_block_data = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)
        self.assertEqual(self.ina._gain, self.ina.GAIN_1_40MV)
        self.assertTrue(self.ina._auto_gain_enabled)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_manual_gain_no_expected_amps(self):
        self.ina = INA219(0.1)
        self.ina._pi = Mock()
        self.ina._i2c_handle = HANDLE
        self.ina._pi.i2c_write_i2c_block_data = Mock()
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.assertEqual(self.ina._gain, self.ina.GAIN_1_40MV)
        self.assertFalse(self.ina._auto_gain_enabled)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_auto_gain_out_of_range(self):
        self.ina = INA219(0.1, 4)
        self.ina._pi = Mock()
        with self.assertRaisesRegexp(ValueError, "Expected amps"):
            self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)

    def test_16v_40mv(self):
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.assertEqual(self.ina._gain, 0)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x01, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv(self):
        self.ina.configure(self.ina.RANGE_32V, self.ina.GAIN_1_40MV)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x21, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_80mv(self):
        self.ina.configure(self.ina.RANGE_32V, self.ina.GAIN_2_80MV)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x29, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_160mv(self):
        self.ina.configure(self.ina.RANGE_32V, self.ina.GAIN_4_160MV)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x31, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_320mv(self):
        self.ina.configure(self.ina.RANGE_32V, self.ina.GAIN_8_320MV)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x39, 0x9f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_9bit(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_9BIT, self.ina.ADC_9BIT)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x20, 0x07])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_10_bit_11_bit(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_10BIT, self.ina.ADC_11BIT)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x20, 0x97])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_2_samples_128_samples(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_2SAMP, self.ina.ADC_128SAMP)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x24, 0xff])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_4_samples_8_samples(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_4SAMP, self.ina.ADC_8SAMP)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x25, 0x5f])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_8_samples_16_samples(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_8SAMP, self.ina.ADC_16SAMP)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x25, 0xe7])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_32v_40mv_32_samples_64_samples(self):
        self.ina.configure(
            self.ina.RANGE_32V, self.ina.GAIN_1_40MV,
            self.ina.ADC_32SAMP, self.ina.ADC_64SAMP)
        calls = [call(HANDLE, 0x05, [0x83, 0x33]), call(HANDLE, 0x00, [0x26, 0xf7])]
        self.ina._pi.i2c_write_i2c_block_data.assert_has_calls(calls)

    def test_invalid_voltage_range(self):
        with self.assertRaisesRegexp(ValueError, "Invalid voltage range"):
            self.ina.configure(64, self.ina.GAIN_1_40MV)

    def test_max_current_exceeded(self):
        ina = INA219(0.1, 0.5)
        ina._pi = Mock()
        with self.assertRaisesRegexp(ValueError, "Expected current"):
            ina.configure(ina.RANGE_32V, ina.GAIN_1_40MV)

    def test_sleep(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'0xf'))
        self.ina.sleep()
        self.ina._pi.i2c_read_i2c_block_data.assert_called_with(HANDLE, 0, 2)

    def test_wake(self):
        self.ina._pi.i2c_read_i2c_block_data = Mock(return_value=(1, b'0x8'))
        self.ina.wake()
        self.ina._pi.i2c_read_i2c_block_data.assert_called_with(HANDLE, 0, 2)

    def test_reset(self):
        self.ina.reset()
        self.ina._pi.i2c_write_i2c_block_data.assert_called_with(HANDLE, 0x00, [0x80, 0x00])
