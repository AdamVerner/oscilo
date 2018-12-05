# /bin/env python3
# -*- coding: utf-8 -*-
"""
dummy fpga for testing and development of user app

always replies with same waveforms and so on....
"""

import numpy as np

from Exceptions import OutOfInitState


class Device(object):

    STATE_INIT = 0x00
    STATE_SAMPLE_MEM_READER = 0x02
    STATE_SAMPLER = 0x04
    STATE_CONFIG_READ = 0x08
    STATE_CONFIG_WRITE = 0x10

    _state = STATE_INIT

    sample_speed = 2

    def __init__(self):
        self.log_data = list()  # each line is one information of device log
        self.state = self.STATE_INIT

    def get_samples(self, samples):
        self.state = self.STATE_SAMPLE_MEM_READER

        x = np.arange(samples)  # the points on the x axis for plotting
        # compute the value (amplitude) of the sin wave at the for each sample
        y = [np.sin(2*np.pi*self.sample_speed * (i/samples)) for i in x]

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
        self.log('received: %s ' % data[:n-1])

    def serial_write(self, data):
        self.log('writing to device: %s' % data)

    def log(self, info):
        # TODO add timestamps
        print(info)
        self.log_data.append(info)


if __name__ == '__main__':

    D = Device()
    print(D.state)
    print(D.get_samples(512))
