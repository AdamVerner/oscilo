#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from serial import Serial
import unittest

"""
some tests to run on final device
"""


class MainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.serial_device = Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)

    @classmethod
    def tearDownClass(cls):
        cls.serial_device.close()

    def setUp(self):
        self.serial_device.reset_input_buffer()
        self.serial_device.reset_output_buffer()

    def test_replayer_1(self):
        self.serial_device.write(b'\x71')  # replayer state ID

        self.assertEqual(self.serial_device.read(1), b'')  # assert that the device sent nothing

        for data in [b'\x01', b'\x32', b'\x25', b'\x33', b'\x43', b'\xf5', b'\xff', b'\x00']:
            self.serial_device.write(data)
            self.assertEqual(data, self.serial_device.read(1))

        self.serial_device.write(b'\x55')  # turn the replayer off
        self.assertEqual(self.serial_device.read(1), b'\x55')  # device should reply with 0x55
        self.assertEqual(self.serial_device.read(1), b'')  # now the device should be quiet

    # device should be able to do the same thing two times
    test_replayer_again = test_replayer_1

    def test_reply_cnt(self):
        self.serial_device.write(b'\x72')  # select module

        self.serial_device.write(b'\x2a')  # 2a = dec(42)
        for number in range(0, 42, 1):
            self.assertEqual(self.serial_device.read(1), chr(number).encode('utf-8'))


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None

    suite = test_loader.loadTestsFromTestCase(MainTest)

    test = unittest.TextTestRunner(verbosity=2)
    result = test.run(suite)

    print('success', result.wasSuccessful())
    print('testRun', result.testsRun)
