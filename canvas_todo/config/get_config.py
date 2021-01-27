import os
from typing import Dict

import yaml

from .config_paths import APP_CONF_PATH, GKEEP_CONF_PATH, CANVAS_CONF_PATH

def get_app_config() -> Dict:
    """Gets app config from file

    Returns
    -------
    Dict
        application config dictionary
    """
    return _get_config(APP_CONF_PATH)


def get_gkeep_config() -> Dict:
    """Gets google keep config from file

    Returns
    -------
    Dict
        google keep config dictionary
    """
    return _get_config(GKEEP_CONF_PATH)


def get_canvas_config() -> Dict:
    """Gets canvas config from file

    Returns
    -------
    Dict
        canvas config dictionary
    """
    return _get_config(CANVAS_CONF_PATH)


def _get_config(conf_path: os.PathLike) -> Dict:
    """Gets yaml config at path

    Parameters
    ----------
    conf_path : os.PathLike
        path to yaml config

    Returns
    -------
    Dict
        contents of yaml config, as dict
    """
    with open(conf_path, "r") as conf_file:
        return yaml.load(conf_file, Loader=yaml.Loader)
