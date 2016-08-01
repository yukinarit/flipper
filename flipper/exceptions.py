import enum

__all__ = [
    'FlipperException',
    'InvalidSlackParam',
    'SlackConnectionFailuer',
]


class ExitCode(enum.IntEnum):
    Success = 0
    Error = 1
    InvalidSlackParam = 10
    SlackConnectionFailuer = 11


class FlipperException(Exception):
    def __init__(self, msg=None):
        super(FlipperException, self).__init__(msg)
        self.code = ExitCode.Error


class InvalidSlackParam(FlipperException):
    def __init__(self, msg=None):
        super(InvalidSlackParam, self).__init__(msg)
        self.code = ExitCode.InvalidSlackParam


class SlackConnectionFailuer(FlipperException):
    def __init__(self, msg=None):
        super(SlackConnectionFailuer, self).__init__(msg)
        self.code = ExitCode.SlackConnectionFailuer
