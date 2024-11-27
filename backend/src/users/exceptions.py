class UserAlreadyExists(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserDoesNotHavePermission(Exception):
    pass
