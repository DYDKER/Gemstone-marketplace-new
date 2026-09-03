class UserNotFoundError(Exception):
    pass


class StoneNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class StoneAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass
