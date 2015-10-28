#encoding:utf-8
__author__ = 'binpo'

from tornado.options import define, options

def parse_config_file(path):
    """Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.

    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    execfile(path, config, config)
    for name in config:
        # define(name, config[name])
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])

