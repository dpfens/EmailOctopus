class EmailOctopusException(Exception):
    error_code = None
    """
    A base exception for exceptions raised by the EmailOctopus API

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(EmailOctopusException, self).__init__(message)
        self.code = code


class InvalidParametersException(EmailOctopusException):
    error_code = 'INVALID_PARAMETERS'
    """
    Parameters are missing or invalid.

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(InvalidParametersException, self).__init__(code, message)


class InvalidKeyException(EmailOctopusException):
    error_code = 'API_KEY_INVALID'
    """
    API key is invalid

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(InvalidKeyException, self).__init__(code, message)


class UnauthorisedException(EmailOctopusException):
    error_code = 'UNAUTHORISED'
    """
    Not authorised to perform the action

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(UnauthorisedException, self).__init__(code, message)


class NotFoundException(EmailOctopusException):
    errorcode = 'NOT_FOUND'
    """
    Requested endpoint does not exist

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(NotFoundException, self).__init__(code, message)


class UnknownException(EmailOctopusException):
    error_code = 'UNKNOWN'
    """
    Unknown error has occurred

    Attributes:
        code (str): The code indicating the type of exception that occurred
        message (str): Explanation of why the exception was raised
    """

    def __init__(self, code, message):
        super(UnknownException, self).__init__(code, message)
