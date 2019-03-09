# /bin/env python3
# -*- coding: utf-8 -*-

"""
Main class for handling communication with FPGA Board
"""
import logging
import os
from multiprocessing import Process
from time import sleep
from typing import List, Callable

from serial import Serial, SerialException

from Software.Devices.Exceptions import *
from Software.Popups import task_fail, PortSelector

root_logger = logging.getLogger(__name__)


class TrigModes(object):
    RISE = b'\x01'
    FALL = b'\x02'
    BOTH = b'\x03'
    NONE = b'\x04'

    @staticmethod
    def get_str(mode):
        if mode == b'\x01':
            return 'RISE'
        if mode == b'\x02':
            return 'FALL'
        if mode == b'\x03':
            return 'BOTH'
        if mode == b'\x04':
            return 'NONE'
        raise ValueError('unknown mode')


class Device(object):
    """
    test text of long description
    """

    description = 'device used to measure voltage'
    name = 'Osciloscope'
    icon = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/oscilloscope.png'))

    HAS_VERTICAL = False

    TRIG_MODES = TrigModes()

    MAX_SPEED = 50000000  # 50Mhz samplping clock
    MIN_SPEED = 50000000 / 65535

    sample_count = 256  # maximum number of samples the device can store
    sampling_speed = MAX_SPEED

    _trigger_mode = TRIG_MODES.RISE
    _upper_bound = b'\x80'
    _lower_bound = b'\x80'

    trig_max = 255
    trig_min = 0
    trig_step = 1

    _SAMPLER = b'\x21'
    _SAMPLE_READ = b'\x22'
    _MEM_CLEAR = b'\x23'
    _OFFSET_GETTER = b'\x24'
    _ADC_SELECTOR = b'\x25'
    _TRIG_CONFIG = b'\x31'
    _CLK_CFG = b'\x32'
    _REPLAYER = b'\x71'
    _REPLY_CNT = b'\x72'

    available = False

    def __new__(cls) -> object:
        """
        initializes USB serial communication port
        asserts, that the device is ready and responding.
        if there are means it should calibrate the device
        """

        try:
            instance = super().__new__(cls)
            instance.log = root_logger.getChild(cls.__class__.__name__)

            port = PortSelector().get_selection()

            instance._dev = Serial(port=port, baudrate=115200, timeout=1)
            instance._dev.reset_input_buffer()
            instance._dev.reset_output_buffer()
            instance.available = True
            instance.comm_test()
            instance.log.info('device passed initial tests')
            return instance
        except (SerialException, DeviceTestError):
            root_logger.exception('connecting do Hardware failed, returning dummy instead, '
                                  'dumping traceback and returning Dummy instead')
            task_fail('Cannot open device port %s' % port, 'returning dummy device instead')

            from Software.Devices.Dummy import Device as Dev
            return Dev()

    def __init__(self):
        pass

    def comm_test(self) -> None:
        self.log.info('testing the device')

        expected = b''.join([chr(number).encode('utf-8') for number in range(0, 0x05, 1)])
        self.log.debug('received data should be %s ', expected)

        self._dev.write(self._REPLY_CNT)  # select module
        self._dev.write(b'\x05')  # 2a = dec(42)
        data = self._dev.read(0x05)
        self.log.debug('received data from device %s', data)

        if data != expected:
            raise DeviceTestError('recieved invalid data, see logs')

    def destroy(self) -> None:
        """
        cleans up device
        closes serial port
        """
        self.set_memory_to(b'\x49')  # random byte

    def set_memory_to(self, word: bytes) -> None:
        """
        :param word: e.g.: b'\x32'
        """

        self._dev.write(self._MEM_CLEAR)
        sleep(0.1)
        self._dev.write(word)

    def get_samples(self) -> List[int]:

        self._dev.flushInput()

        self._dev.write(self._SAMPLE_READ)  # start sample-reader
        buf = b''

        # fix issue with deep sample memory
        while True:
            b = self._dev.read(65535)
            if not len(b):
                break
            buf += b

        msbs = buf[::2]
        lsbs = buf[1::2]

        print(msbs)
        print(lsbs)

        samples = [(int(msb) << 8) + int(lsb) for msb, lsb in zip(msbs, lsbs)]

        self.log.info('num of samples = %d', len(samples))

        if len(samples) != self.sample_count:
            raise CommunicationError('not all samples were received')

        offset = self.get_sample_offset() + self.sample_count

        # assume 50% trigger placement
        start = offset - self.sample_count // 2
        stop = offset + self.sample_count // 2

        post = (samples + samples + samples)[start:stop]  # place trigger point where it should be
        post = [int(x) for x in post]

        # post = [int('{:12b}'.format(n)[::-1], 2) for n in post]

        print(post, samples, '\n\n')
        print('#' * 50, 'average value is: ', sum(post) / len(post))
        print('#' * 50, 'min value is:     ', min(post))
        print('#' * 50, 'max value is:     ', max(post), '\n\n\n')
        return post

    def get_sample_offset(self) -> int:

        self._dev.write(self._OFFSET_GETTER)
        offset = self._dev.read(4)
        offset = int(offset.hex(), 16)
        return offset

    def get_trig_lvl(self) -> int:
        if self._trigger_mode == self.TRIG_MODES.FALL:
            return int(self._lower_bound.hex(), 16) >> 8
        else:
            return int(self._upper_bound.hex(), 16) >> 8

    def set_trig_lvl(self, level: int) -> None:
        self._upper_bound = bytes([int(level)])
        self._lower_bound = bytes([int(level)])
        self.log.info('setting trigger to: %s and %s', self._upper_bound, self._lower_bound)

        self._set_trig_modes(self._trigger_mode, self._upper_bound, self._lower_bound)

    def get_trigger_mode(self) -> int:
        return int(self._trigger_mode.hex(), 16)

    def set_trigger_mode(self, mode: bytes) -> None:
        self.log.info('trigger mode has been set to: %s' % mode)
        # TODO verify if mode is legit
        self._trigger_mode = mode
        self._set_trig_modes(self._trigger_mode, self._upper_bound, self._lower_bound)

    def set_bound(self, upper: int, lower: int) -> None:
        """set bound for trigger windows"""
        self._upper_bound = bytes([int(upper)])
        self._lower_bound = bytes([int(lower)])

        self._set_trig_modes(self._trigger_mode, self._upper_bound, self._lower_bound)

    def _set_trig_modes(self, mode: bytes, upper: bytes, lower: bytes) -> None:
        print('setting trigger', self._TRIG_CONFIG, mode, upper, lower)
        self._dev.write(self._TRIG_CONFIG)
        self._dev.write(mode)
        self._dev.write(upper)
        self._dev.write(lower)

    def activate_scope(self, sampling_callback: Callable, done_callback: Callable) -> None:
        """
        :param sampling_callback: function to call when the scope transitions into post_trigger
        :param done_callback:  function to call when scope is done with measurements
        """

        self._dev.write(self._ADC_SELECTOR)
        self._dev.write(b'\x03')  # choose adc
        self._dev.write(self._SAMPLER)

        sampling_callback()

        def logic(*_):
            while True:
                resp = self._dev.read(1)
                print('waiting for scope to trigger, received : %s', resp)
                if resp == b'\x55':
                    print('received end, breaking')
                    break
            done_callback()

        Process(target=logic).start()

    @staticmethod
    def get_closests(arr, target):
        n = len(arr)
        left = 0
        right = n - 1
        mid = 0

        # edge case - last or above all
        if target >= arr[n - 1]:
            return arr[n - 1]
        # edge case - first or below all
        if target <= arr[0]:
            return arr[0]
        # BSearch solution: Time & Space: Log(N)

        while left < right:
            mid = (left + right) // 2  # find the mid
            if target < arr[mid]:
                right = mid
            elif target > arr[mid]:
                left = mid + 1
            else:
                return arr[mid]

        if target < arr[mid]:
            return arr[mid] if target - arr[mid - 1] >= arr[mid] - target else arr[mid - 1]
        else:
            return arr[mid + 1] if target - arr[mid] >= arr[mid + 1] - target else arr[mid]

    def set_sampling_speed(self, speed):
        """
        :param speed: speed to set in herz
        :return: actual sampling speed, that was set
        """
        ls = [50000000 // div for div in range(1, 65553)][::-1]
        selected = self.get_closests(ls, speed)
        divison = self.MAX_SPEED // selected - 1

        lsb = divison & 0xff
        msb = (divison >> 8) & 0xff

        print(msb, lsb)

        self._dev.write(self._CLK_CFG)
        self._dev.write(bytes([int(msb)]))  # LSB
        self._dev.write(bytes([int(lsb)]))  # MSB

        self.sampling_speed = selected
        return selected

    def get_sampling_speed(self):
        return self.sampling_speed

    def get_trig_place(self):
        return 0.5
