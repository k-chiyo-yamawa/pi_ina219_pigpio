import sys
import logging
import unittest
from ina219 import INA219

logger = logging.getLogger()
logger.level = logging.ERROR
logger.addHandler(logging.StreamHandler(sys.stdout))


class TestConstructor(unittest.TestCase):

    def test_default(self):
        self.ina = INA219(0.1)
        self.assertEqual(self.ina._shunt_ohms, 0.1)
        self.assertIsNone(self.ina._max_expected_amps)
        self.assertIsNone(self.ina._gain)
        self.assertFalse(self.ina._auto_gain_enabled)
        self.assertAlmostEqual(self.ina._min_device_current_lsb, 6.25e-6, 2)

    def test_with_max_expected_amps(self):
        self.ina = INA219(0.1, 0.4)
        self.assertEqual(self.ina._shunt_ohms, 0.1)
        self.assertEqual(self.ina._max_expected_amps, 0.4)
