# pylint: disable=missing-docstring

from re import findall

def map_err_message(err, message):
    """
    Decorator that maps a specific error to a custom error message.

    Args:
        err (Exception): The specific error to catch.
        message (str): The custom error message to raise.

    Returns:
        The decorated function.

    Raises:
        ValueError: If the specified error is raised,
        it is caught and a ValueError with the custom error message
        is raised instead.
    """
    def dec(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except err:
                raise ValueError(message)

        return inner
    return dec

def return_err_message(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            return err

    return inner

def validate_args_array(template):
    def dec(func):
        fargs = findall(r"<[^>]+>", template)

        def inner(*args, **kwargs):
            if len(args[0]) < len(fargs):
                raise ValueError(f"Not enough arguments, expected: {template}")

            return func(*args, **kwargs)

        return inner
    return dec

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args