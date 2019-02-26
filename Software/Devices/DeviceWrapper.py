import logging

import Software.Devices.Dummy
import Software.Devices.L1V1

root_logger = logging.getLogger(__name__)


class DeviceWrapper(object):
    """
    Class to use as a major Device.

    Allows changing devices on the go.
    """

    def __init__(self):
        self._dev = Software.Devices.Dummy.Device()  # default device

        self._log = root_logger.getChild(self.__class__.__name__)

        self._avail = [  # list of all available devices
            Software.Devices.Dummy.Device,
            Software.Devices.L1V1.Device,
        ]

    def get_available(self):
        """
        :return: all available devices information
        """
        # TODO change API to return dict with specified parameters
        return self._avail

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
