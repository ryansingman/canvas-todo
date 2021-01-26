import os
from typing import Dict
from datetime import datetime, timezone

import keyring
import yaml
from canvasapi import Canvas

from .config_paths import APP_CONF_PATH, GKEEP_CONF_PATH, CANVAS_CONF_PATH


def gen_config():
    """Generates yaml config from user input
    """
    # create config dir if it doesn't exist
    os.makedirs(os.path.split(APP_CONF_PATH)[0], exist_ok=True)

    # generate configs
    gen_gkeep_config()
    canvas_conf = gen_canvas_config()
    gen_app_config(canvas_conf)

def gen_app_config(canvas_conf: Dict) -> Dict:
    """Generates yaml config from user input for app operation

    Paramters
    ---------
    canvas_conf : Dict
        canvas configuration dictionary, used to get classes to monitor

    Returns
    -------
    Dict
        app config dictionary
    """
    # check for existing app config
    if (
            os.path.exists(APP_CONF_PATH) and
            (input("Delete existing app config and restart [Y/n]?: ").lower() == "n")
    ):
        return None

    # init app conf
    app_conf = {}

    # get update rate [default: 30 min]
    app_conf["update_rate"] = float(input("App update rate in minutes [default: 30 min]: ") or 30)

    # get if should print to console
    app_conf["console_print"] = input("Print to console [Y/n]?: ").lower() != "n"

    # create canvas obj
    canv = Canvas(
        canvas_conf["api_url"],
        keyring.get_password('canvas-token', canvas_conf["api_username"])
    )

    # get classes to watch
    # NOTE: only prompts for active courses with start dates within the last 6 months
    app_conf["classes"] = []
    for course in canv.get_courses(enrollment_state="active"):
        time_delt = datetime.now(timezone.utc) - datetime.strptime(course.created_at, "%Y-%m-%dT%H:%M:%S%z")
        if time_delt.days < (6*30) and input(f"Include {course.name} [Y/n]?: ").lower() != "n":
            app_conf["classes"].append(course.id)

    # get assignment config
    app_conf["assignments_conf"] = {
        "due_date_horizon": int(input("Due date horizon in days [default: 21 days]: ") or 21)
    }

    # dump config
    with open(APP_CONF_PATH, "w") as app_conf_out:
        yaml.dump(app_conf, app_conf_out)

    return app_conf


def gen_gkeep_config():
    """Generates yaml config from user input for google keep interface
    """
    # check for existing gkeep config
    if (
            os.path.exists(GKEEP_CONF_PATH) and
            (input("Delete existing google keep config and restart [Y/n] ?: ").lower() == "n")
    ):
        with open(GKEEP_CONF_PATH, "r") as gkeep_conf_in:
            return yaml.load(gkeep_conf_in)

    # init gkeep conf
    gkeep_conf = {}

    # get API url, username, key
    gkeep_conf["api_url"] = input("Google Keep URL: ")
    gkeep_conf["api_username"] = input("Google Keep Username: ")
    keyring.set_password('gkeep-token', gkeep_conf["api_username"], input("Google Keep Key: "))

    return gkeep_conf


def gen_canvas_config() -> Dict:
    """Generates yaml config from user input for canvas interface

    Returns
    -------
    Dict
        canvas config dict
    """
    # check for existing canvas config
    if (
            os.path.exists(CANVAS_CONF_PATH) and
            (input("Delete existing canvas config and restart [Y/n] ?: ").lower() == "n")
    ):
        with open(CANVAS_CONF_PATH, "r") as canvas_conf_in:
            return yaml.load(canvas_conf_in)

    # init canvas conf
    canvas_conf = {}

    # get API url, username, key
    canvas_conf["api_url"] = input("Canvas URL: ")
    canvas_conf["api_username"] = input("Canvas Username: ")
    keyring.set_password('canvas-token', canvas_conf["api_username"], input("Canvas Key: "))

    # dump config
    with open(CANVAS_CONF_PATH, "w") as canvas_conf_out:
        yaml.dump(canvas_conf, canvas_conf_out)

    return canvas_conf
