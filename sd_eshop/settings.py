import os
import pathlib
import argparse

import trafaret as T
from trafaret_config import commandline, simple


BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'local.yaml'

CONFIG_TRAFARET = T.Dict({
    T.Key('mongo'):
        T.Dict({
            T.Key('database', optional=True): T.String(),
            T.Key('username', optional=True): (T.String(allow_blank=True)),
            T.Key('password', optional=True): (T.String(allow_blank=True)),
            'host': T.String(),
            'port': T.Int(),
        }),
    T.Key('host', optional=True): T.IP,
    T.Key('port', optional=True): T.Int(),
})


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=os.environ.get(
            'AIOHTTP_SETTINGS_PATH', DEFAULT_CONFIG_PATH)
    )

    options, _ = ap.parse_known_args(argv)

    envs = _get_config_vars(options, CONFIG_TRAFARET)

    config = commandline.config_from_options(
        options,
        CONFIG_TRAFARET,
        envs
    )
    return config


def _get_config_vars(options, trafaret):
    config_vars = simple.read_and_get_vars(options.config, trafaret)

    return {var: os.environ.get(var) for var in config_vars}
