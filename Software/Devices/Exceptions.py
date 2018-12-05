# /bin/env python3
# -*- coding: utf-8 -*-


class BaseDeviceException(Exception):
    """
    Basic exception of
    """


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
