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
        self._dev = get_available_devices()[0]()

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
            return self.__getattribute__(attr)
        except AttributeError:
            try:
                return self._dev.__getattribute__(attr)
            except AttributeError:
                self._log.critical('%s requested unset atribute, returning universal handler', attr)
                return self._universal_handler

    def _universal_handler(self, *args, **kwargs):
        """
        Handle a command that was not specified anywhere
        """
        print("My arguments are: " + str(args))
        print("My keyword arguments are: " + str(kwargs))
        # raise Warning('this method should never be called')


class GenericDevice(object):
    """
    This devices doesn't do anything, it's only purpose is to provide some default values for
    each new device, like description and such.
    """
    description = "generic device used to subclass other devices"
