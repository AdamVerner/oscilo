# /bin/env python3
# -*- coding: utf-8 -*-


class BaseDeviceException(Exception):
    """
    Basic exception of
    """


class UserRequestError(BaseException):
    """invalid request for device, it's your fault"""


class CommunicationError(BaseDeviceException):
    """
    exceptions usually raised by invalid reply from device
    """


class InvalidReply(CommunicationError):
    """
    Device replied with some bullshit
    """


class InternalError(BaseDeviceException):
    """
    when something just doesn't work as it should....
    """


class OutOfInitState(BaseDeviceException):
    """
    Device is not in init state and something tried to set state.
    """


class DeviceTestError(CommunicationError):
    """
    The device didn't pass some mandatory tests, that verify the functionality of the device
    """
