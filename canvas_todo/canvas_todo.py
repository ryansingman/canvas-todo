import threading
from datetime import datetime
from typing import Any, Dict, List

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.assignment import Assignment
from colored import fore, style

from .assignments import get_assignments
from .utils import get_courses_from_ids
from .config import get_app_config, get_canvas_config   #, get_gkeep_config

class CanvasTodo(threading.Thread):
    """CanvasTodo main class
    """
    canvas_conf: Dict[Any, Any]
    canv: Canvas
    courses = List[Course]

    def __init__(self):
        """Initializes CanvasTodo class
        """
        # init thread
        super().__init__()

        # get canvas conf
        self.canvas_conf = get_canvas_config()

        # get app conf
        self.app_conf = get_app_config()

        # create canvas obj
        self.canv = Canvas(self.canvas_conf["api_url"], self.canvas_conf["api_key"])

        # get user
        self.user = self.canv.get_current_user()

        # get list of courses
        self.courses = get_courses_from_ids(self.canv, self.app_conf["classes"])

    def run(self):
        """Runs CanvasTodo thread

        Get assignments, (maybe) prints to console, (tbd) updates todo list on google keep
        """
        # inf run loop
        while True:
            # get updated assignments
            assignments = get_assignments(self.courses, **self.app_conf["assignments_conf"])

            # print assignments
            if self.app_conf["console_print"]:
                self.print_assignments(assignments)

            input("Any key to continue")


    def print_assignments(self, asssignments: Dict[Course, List[Assignment]]):
        """Pretty prints assignments for each course

        Parameters
        ----------
        asssignments : Dict[Course, List[Assignment]]
            assignments to print
        """
        for course, course_assignments in asssignments.items():
            print(f"{fore.GREEN} {style.BOLD} {course.name}: {style.RESET}")

            # print each assignment
            for assmnt in course_assignments:
                # get due date string for assignment
                due_date_str = datetime.strptime(
                    assmnt.due_at, "%Y-%m-%dT%H:%M:%S%z"
                ).strftime("%Y-%m-%d %H:%M")

                # get submitted string for assignment
                if assmnt.submission_types == ['none']:
                    submitted_str = "?"
                elif not assmnt.get_submission(self.user).submitted_at is None:
                    submitted_str = "x"
                else:
                    submitted_str = " "

                # print formatted assignment string
                print(f"\t[{submitted_str}] {due_date_str:^16}: {assmnt.name:<80}")
