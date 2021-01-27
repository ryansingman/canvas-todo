import os
from typing import Dict
from datetime import datetime, timezone

import keyring
import yaml
import gkeepapi
from getpass import getpass
from canvasapi import Canvas

from .config_paths import APP_CONF_PATH, GKEEP_CONF_PATH, CANVAS_CONF_PATH
from ..utils import time_utils


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
            (input("Delete existing app config and restart [y/N]?: ").lower() != "y")
    ):
        with open(APP_CONF_PATH, "r") as app_conf_in:
            return yaml.load(app_conf_in, Loader=yaml.Loader)

    # init app conf
    app_conf = {}

    # get update rate [default: 30 min]
    app_conf["update_rate"] = 60 * float(input("App update rate in minutes [default: 30 min]: ") or 30)

    # get if should print to console
    app_conf["console_print"] = input("Print to console [Y/n]?: ").lower() != "n"

    # create canvas obj
    canv = Canvas(
        canvas_conf["api_url"],
        keyring.get_password('canvas-token', canvas_conf["api_username"])
    )

    # init classes dict
    app_conf["classes"] = {}

    # init colors
    colors = [c.name for c in gkeepapi.node.ColorValue]
    color_idx = 0
    print(f"Possible course colors:\n  {colors}")

    # get classes to watch
    # NOTE: only prompts for active courses with start dates within the last 6 months
    for course in canv.get_courses(enrollment_state="active"):
        # get time delta
        time_delt = datetime.now(timezone.utc) - time_utils.from_iso8601(course.created_at)

        # check if should include course
        if time_delt.days < (6*30) and input(f"Include {course.name} [Y/n]?: ").lower() != "n":
            # get course parameters
            app_conf["classes"][course.id] = {
                "nickname": input(f"  Course Nickname [default: {course.name}]: ") or course.name,
                "color": getattr(
                    gkeepapi.node.ColorValue,
                    (
                        input(f"  Color (default: {colors[color_idx % len(colors)]}): ") or
                        colors[color_idx % len(colors)]
                    )
                )
            }

            # increment color idx
            color_idx += 1

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
            (input("Delete existing google keep config and restart [y/N] ?: ").lower() != "y")
    ):
        with open(GKEEP_CONF_PATH, "r") as gkeep_conf_in:
            return yaml.load(gkeep_conf_in, Loader=yaml.Loader)

    # init gkeep conf
    gkeep_conf = {}

    # get API username, key
    gkeep_conf["api_username"] = input("Google Keep Username: ")
    keep = gkeepapi.Keep()
    keep.login(gkeep_conf["api_username"], getpass("Google Keep Password: "))
    keyring.set_password('gkeep-key', gkeep_conf["api_username"], keep.getMasterToken())

    # get if should pin course notes
    gkeep_conf["pin_notes"] = input("Pin notes [Y/n]?: ").lower() == n

    # dump config
    with open(GKEEP_CONF_PATH, "w") as gkeep_conf_out:
        yaml.dump(gkeep_conf, gkeep_conf_out)

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
            (input("Delete existing canvas config and restart [y/N] ?: ").lower() != "y")
    ):
        with open(CANVAS_CONF_PATH, "r") as canvas_conf_in:
            return yaml.load(canvas_conf_in, Loader=yaml.Loader)

    # init canvas conf
    canvas_conf = {}

    # get API url, username, key
    canvas_conf["api_url"] = input("Canvas URL: ")
    canvas_conf["api_username"] = input("Canvas Username: ")
    keyring.set_password('canvas-token', canvas_conf["api_username"], getpass("Canvas Key: "))

    # dump config
    with open(CANVAS_CONF_PATH, "w") as canvas_conf_out:
        yaml.dump(canvas_conf, canvas_conf_out)

    return canvas_conf
