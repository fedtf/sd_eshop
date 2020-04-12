import pathlib
import argparse

import trafaret as T
from trafaret_config import commandline


BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'settings.yaml'

CONFIG_TRAFARET = T.Dict({
    T.Key('mongo'):
        T.Dict({
            T.Key('database', optional=True): T.String(),
            T.Key('username', optional=True): T.String(),
            T.Key('password', optional=True): T.String(),
            'host': T.String(),
            'port': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    options, _ = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, CONFIG_TRAFARET)
    return config
