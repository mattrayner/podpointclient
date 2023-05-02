"""Custom errors"""

class APIError(Exception):
    """The most generic APIError"""

class AuthError(APIError):
    """An error relating to authentication with pod point"""
    def __init__(self, status, response):
        message = f'Auth Error ({status}) - {response}'
        super().__init__(message)

class SessionError(APIError):
    """An error relating to session creation with pod point"""
    def __init__(self, status, response):
        message = f'Session Error ({status}) - {response}'
        super().__init__(message)

class ApiConnectionError(APIError):
    """An error relating to connecting to pod point"""
    def __init__(self, message):
        super().__init__(f'Connection Error: {message}')

class ChargeOverrideValidationError(Exception):
    """An error relating to connecting to pod point"""
    def __init__(self):
        super().__init__(f'A validate error occured when processing charge override. Please ensure that an hour, minute or second value is passed and that it is > 0.')
