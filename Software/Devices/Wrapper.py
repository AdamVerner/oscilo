import logging

import Software.Devices.Dummy
import Software.Devices.L1V1

root_logger = logging.getLogger(__name__)


def get_available_devices():
    devices = [  # list of all available devices
        Software.Devices.Dummy.Device,
        Software.Devices.L1V1.Device,
    ]

    return devices


class DeviceWrapper(object):
    """
    Class to use as a major Device.

    Allows changing devices on the go.
    """

    def __init__(self):
        self.default_device = Software.Devices.L1V1.Device()
        self._dev = self.default_device

        self._log = root_logger.getChild(self.__class__.__name__)

    def __setattr__(self, name, value):
        self.__dict__[name] = value  # assigning to the dict of names in the class
        # define custom behavior here

    def __getattr__(self, attr):
        """
        first try to look through own functions, if the corresponding attribute isn't there,
        look through device
        """
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            print('attr %s not found in self, looking it up in dev' % attr)
            try:
                return self._dev.__getattribute__(attr)
            except AttributeError:
                self._log.critical('%s requested unset attribute, returning universal handler',
                                   attr)
                return self._universal_handler

    @staticmethod
    def _universal_handler(*args, **kwargs):
        """
        Handle a command that was not specified anywhere
        """
        print("My arguments are: " + str(args))
        print("My keyword arguments are: " + str(kwargs))
        # raise Warning('this method should never be called')

    def change_device(self, device):
        print('changing to new device %s' % device)
        self._dev = device()
        print('changed to ', self._dev)
        return self._dev


class GenericDevice(object):
    """
    This devices doesn't do anything, it's only purpose is to provide some default values for
    each new device, like description and such.
    """
    description = "generic device used to subclass other devices"
