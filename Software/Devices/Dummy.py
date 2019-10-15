# /bin/env python3
# -*- coding: utf-8 -*-
"""
dummy fpga for testing and development of user app

always replies with same waveforms and so on....
"""

import os
from multiprocessing import Process
from random import randint
from time import sleep
from typing import List, Callable

from numpy import arange, sin, pi

from Software.Devices.L1V1 import TrigModes


class Device(object):
    """
    <span foreground="blue" size="x-large">DUMMY DEVICE</span>
    This device simulates all possible options, that a device can have.
    Samples are genereated randomly as they're only for testing graph generat viewing purposes.
    That means, that trigger options don't usally match
    """

    description = 'all interfaces available, some of them do something'
    name = 'DUMMY'
    icon = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/fake_news.png'))

    HAS_VERTICAL = False

    TRIG_MODES = TrigModes()

    trig_max = 127
    trig_min = -127
    trig_step = 1

    MAX_SPEED = 50000000  # 50Mhz samplping clock
    MIN_SPEED = 50000000 / 65535

    sample_count = 255  # maximum number of samples the device can store
    sampling_speed = MAX_SPEED


    _trig_mode = TRIG_MODES.RISE
    _mem = b'\x10' * sample_count
    _trigger_level = 0x80
    _trig_place = 0.5

    def __init__(self):
        pass

    def destroy(self) -> None:
        pass

    def set_memory_to(self, word: bytes) -> None:
        self._mem = word * self.sample_count

    def get_samples(self) -> List[int]:
        return [int(x) for x in self._mem]

    get_sample_offset = lambda: 0

    def get_trig_lvl(self) -> int:
        return self._trigger_level

    def set_trig_lvl(self, level: int) -> None:
        self._trigger_level = level

    def get_trigger_mode(self) -> int:
        return self.TRIG_MODES.get_str(self._trig_mode)

    def set_trigger_mode(self, mode: bytes) -> None:
        self._trig_mode = mode

    def set_bound(self, upper: int, lower: int) -> None:
        pass

    def get_trig_place(self) -> float:
        """
        :returns: 0-1 according to trigger placement
        """
        return self._trig_place  # 50% default

    def set_trig_place(self, value: float) -> None:
        self._trig_place = value

    def __init__(self, *_, **__):
        self.log_data = list()  # each line is one information of device log
        # self.set_memory_to(b'\x00')

    def activate_scope(self, sampling_callback: Callable = None, done_callback: Callable = None):
        """
        :param sampling_callback: function to call when the scope transitions into post_trigger
        :param done_callback:  function to call when scope is done with measurements
        """

        x = arange(self.sample_count)  # the points on the x axis for plotting
        # compute the value (amplitude) of the sin wave at the for each sample
        y = [sin(4 * pi * (i / self.sample_count))* 200 + randint(0, 25) for i in x]

        self._mem = y
        if sampling_callback:
            Process(target=lambda *_: (sleep(0.2), sampling_callback())).start()
        if done_callback:
            Process(target=lambda *_: (sleep(0.4), done_callback())).start()

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
        print('requested speedto be', speed)
        speed = int(speed)
        ls = [50000000 // div for div in range(1, 65553)][::-1]
        selected = self.get_closests(ls, speed)
        self.sampling_speed = selected
        print('returning ', selected)
        return selected

    def get_sampling_speed(self):
        return self.sampling_speed
