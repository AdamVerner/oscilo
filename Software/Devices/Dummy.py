# /bin/env python3
# -*- coding: utf-8 -*-
"""
dummy fpga for testing and development of user app

always replies with same waveforms and so on....
"""

from multiprocessing import Process
from time import sleep
from typing import List, Callable
from numpy import arange, sin, pi
from random import randint, random

from Software.Devices.L1V1 import TrigModes


class Device(object):
    TRIG_MODES = TrigModes()

    sample_count = 255

    trig_max = 255
    trig_min = 0
    trig_step: 1

    _trig_mode = TRIG_MODES.RISE
    _mem = b'\x10' * sample_count
    _trigger_level = 0x80

    def destroy(self) -> None:
        pass

    def set_memory_to(self, word: bytes) -> None:
        self._mem = word * self.sample_count

    def get_samples(self) -> List[int]:
        print('returning samples', self._mem)
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

    def __init__(self, *_, **__):
        self.log_data = list()  # each line is one information of device log
        # self.set_memory_to(b'\x00')

    def activate_scope(self, sampling_callback: Callable, done_callback: Callable):
        """
        :param sampling_callback: function to call when the scope transitions into post_trigger
        :param done_callback:  function to call when scope is done with measurements
        """

        x = arange(self.sample_count)  # the points on the x axis for plotting
        # compute the value (amplitude) of the sin wave at the for each sample
        y = [sin(4 * pi * (i / self.sample_count))*randint(215, 220) * randint(10,
                                                                                        30) for i
             in x]
        print(y)

        self._mem = y

        Process(target=lambda *_: (sleep(0.2), sampling_callback())).start()

        def trg(*_):
            sleep(0.5)
            done_callback()

        Process(target=trg).start()

