from typing import Any, Dict, List

import yaml
from canvasapi import Canvas
from canvasapi.course import Course

from .assignments import get_assignments
from .utils import get_courses_from_ids

class CanvasTodo:
    """CanvasTodo main class
    """
    canvas_conf: Dict[Any, Any]
    canv: Canvas
    courses = List[Course]

    def __init__(self):
        """Initializes CanvasTodo class
        """
        # get canvas conf
        with open(".config/canvas.yaml", "r") as canv_conf_in:
            self.canvas_conf = yaml.load(canv_conf_in)

        # create canvas obj
        self.canv = Canvas(self.canvas_conf["api_url"], self.canvas_conf["api_key"])

        # get user
        self.user = self.canv.get_current_user()

        # get list of courses
        self.courses = get_courses_from_ids(self.canv, self.canvas_conf["classes"])

        x = get_assignments(self.courses)
        for c, a in x.items():
            for ass in a:
                submission = ass.get_submission(self.user)
                print(c.name, ass.name, f"submitted={submission.submitted_at!=None}")
