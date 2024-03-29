#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import logging
import unittest
from time import sleep

from serial import Serial

"""
some tests to run on final device
"""


class MainTest(unittest.TestCase):
    log = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        cls.log.setLevel(logging.DEBUG)
        cls.serial_device = Serial(port='/dev/ttyS9', baudrate=115200, timeout=1)

    @classmethod
    def tearDownClass(cls):
        # noinspection PyUnresolvedReferences
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
        sleep(3.2)

        data = self.serial_device.read(0x2a)

        expected = b''.join([chr(number).encode('utf-8') for number in range(0, 42, 1)])

        self.assertEqual(len(data), len(expected))

        self.assertEqual(data, expected)

    def test_sample_reader(self):

        self.serial_device.write(b'\x22')  # start sample-reader

        samples = self.serial_device.read(1024)  # read all samples
        self.assertEqual(len(samples) // 2 , 256)

    def test_mem_clear(self):
        word = b'\x12'  # select a 1 byte word to test with

        self.serial_device.write(b'\x23')  # enable mem_clear
        self.serial_device.write(word)  # send word to set memmory to

        self.serial_device.write(b'\x22')  # start sample-reader
        samples = self.serial_device.read(1024)  # read all samples
        # samples = [int(x) for x in samples]

        msbs = samples[::2]
        lsbs = samples[1::2]

        self.assertEqual(len(msbs), 256)
        self.assertEqual(len(lsbs), 256)

        joint = [(int(msb) << 8) + int(lsb) for msb, lsb in zip(msbs, lsbs)]
        print(joint)
        self.assertEqual(b'\x00' * 256 , msbs, 'MSBs don\'t match')
        self.assertEqual(word * 256, lsbs, 'lsbs don\'t match')

    def test_offset(self):
        self.serial_device.write(b'\x24')

        recv = self.serial_device.read(16)

        self.log.info('recieved %s as an memmory offset point')

        self.assertEqual(len(recv), 4, 'the offset should be 32bit number, so 4 bytes')



if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None

    suite = test_loader.loadTestsFromTestCase(MainTest)

    test = unittest.TextTestRunner(verbosity=2)
    result = test.run(suite)

    print('success', result.wasSuccessful())
    print('testRun', result.testsRun)
