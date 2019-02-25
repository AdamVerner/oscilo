# /bin/env python3
# -*- coding: utf-8 -*-
"""
dummy fpga for testing and development of user app

always replies with same waveforms and so on....
"""

from multiprocessing import Process
from time import sleep

from Exceptions import OutOfInitState
from numpy import arange, sin, pi


class Device(object):
    STATE_INIT = 0x00
    STATE_SAMPLE_MEM_READER = 0x02
    STATE_SAMPLER = 0x04
    STATE_CONFIG_READ = 0x08
    STATE_CONFIG_WRITE = 0x10

    _state = STATE_INIT

    sample_speed = 2

    _trigger_mode = 'RISING'
    _trigger_modes = ['RISING', 'FALLING', 'BOTH']
    _trigger_level = 128
    trig_max = 255
    trig_min = 0
    trig_step = 1

    # Variable Gain Amplifier
    vga_level = 0  # TODO add setter and getter functions
    vga_max = 255
    vga_min = 0
    vga_step = 4

    # attenuator settings
    att_level = 0  # TODO add setter and getter functions
    # att usually doesn't have that level-variability as vga, so store the values in list

    att_steps = [1, 4, 10, 20]

    offset = 0

    def __init__(self):
        self.log_data = list()  # each line is one information of device log
        self.state = self.STATE_INIT

    def get_samples(self, samples=1024):
        self.state = self.STATE_SAMPLE_MEM_READER

        x = arange(samples)  # the points on the x axis for plotting
        # compute the value (amplitude) of the sin wave at the for each sample
        y = [sin(2 * pi * self.sample_speed * (i / samples)) for i in x]

        # return the state of the device back to init
        self._state = self.STATE_INIT
        self.log('sample memory returned: n=%d %s' % (len(y), repr(y)))
        return y

    def set_sps(self, speed):
        self.log('setting sampling to %d samples per seconds' % speed)
        self.sample_speed = speed

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self.log('changing the state to: %s ' % value)
        if self._state != self.STATE_INIT:
            raise OutOfInitState("device state was requested while the device was not in init")
        self._state = value

    def serial_read(self, n, data):
        """
        workaround for logging the data, that should be red from device
        """
        self.log('received: %s ' % data[:n - 1])

    def serial_write(self, data):
        self.log('writing to device: %s' % data)

    def log(self, info):
        # TODO add timestamps
        print(info)
        self.log_data.append(info)

    @property
    def trigger_mode(self):
        return self._trigger_mode  # TODO poll from device

    @trigger_mode.setter
    def trigger_mode(self, mode):
        self.log('trigger mode has been set to: %s' % mode)
        # TODO verify if mode is legit
        self._trigger_mode = mode

    @property
    def trig_lvl(self):
        return self._trigger_level  # TODO poll from device

    @trig_lvl.setter
    def trig_lvl(self, level):
        self.log('trigger level has been set to: %f' % level)
        self._trigger_level = level

    def activate_scope(self, sampling_callback, done_callback):
        """
        :param sampling_callback: function to call when the scope transitions into post_trigger
        :param done_callback:  function to call when scope is done with measurements
        """

        Process(target=lambda *_: (sleep(2), sampling_callback())).start()

        def trg(*_):
            sleep(4)
            print('set device back to init')
            done_callback()
            print('DONE')

        Process(target=trg).start()

        return


if __name__ == '__main__':
    D = Device()
    print(D.state)
    print(D.get_samples(512))
