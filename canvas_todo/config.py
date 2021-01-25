import os
from datetime import datetime, timezone

import yaml
from canvasapi import Canvas


def gen_config():
    """Generates yaml config from user input
    """
    # check for existing canvas config
    if (
        os.path.exists(".config/canvas.yaml") and
        (input("Delete existing config and restart [Y/n] ?: ").lower() == "n")
    ):
        return None

    # init canvas conf
    canvas_conf = {}

    # get API url, key
    canvas_conf["api_url"] = input("Canvas URL: ")
    canvas_conf["api_key"] = input("Canvas Key: ")

    # create canvas obj
    canv = Canvas(canvas_conf["api_url"], canvas_conf["api_key"])

    # prompt user for classes to watch
    # NOTE: only prompts for active courses with start dates within the last 6 months
    canvas_conf["classes"] = []
    for c in canv.get_courses(enrollment_state="active"):
        td = datetime.now(timezone.utc) - datetime.strptime(c.created_at, "%Y-%m-%dT%H:%M:%S%z")
        if td.days < (6*30) and input(f"Include {c.name} [Y/n]?: ").lower() != "n":
            canvas_conf["classes"].append(c.id)
        
    # dump config
    with open(".config/canvas.yaml", "w") as canvas_conf_out:
        yaml.dump(canvas_conf, canvas_conf_out)
