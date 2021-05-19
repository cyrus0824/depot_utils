import os

def get_env(name: str, default=None, ret_type: type = str):
    """
    Get the value of an environment variable of `name`.

    If `name` is not defined in the environment then the value of
    `default` will be returned if not None.

    The environment variable value is case to `ret_type`.

    :param name: The name of the environment variable.
    :param default: An optional default value if `name` is not defined in the environment.
    :param ret_type:
    :return:
    """
    try:
        v = os.environ[name]
        if ret_type is bool:
            return v.lower() in ["1", "true"]
        return ret_type(v)
    except KeyError:
        if default is not None:
            return default
        raise
