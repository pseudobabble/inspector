import os

# this is a dumb way to implement this but it's fun.
env = lambda init, key, default=None: init(os.getenv(key, default))
env.__doc__ = """
A convenience function for expressing typed env config consistently

:param init: Callable, The constructor (usually type) of the env var.
:param key: str, The name of the env var
:param default: The value to return if the env var is not set.
:return: The environment variable initialised to the desired type.
"""
