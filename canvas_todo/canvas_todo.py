import threading
import collections
from typing import Any, Dict, List
from time import sleep

import keyring
from canvasapi import Canvas
from canvasapi.course import Course
from colored import fore, style

from .todo import GKeep, Task, Completed, Update
from .assignments import get_assignments
from .utils import get_courses_from_ids
from .config import get_app_config, get_canvas_config, get_gkeep_config


class CanvasTodo(threading.Thread):
    """CanvasTodo main class
    """
    canvas_conf: Dict[str, Any]
    app_conf: Dict[str, Any]
    gkeep_conf: Dict[str, Any]
    canv: Canvas
    todo: GKeep
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

        # get gkeep conf
        self.gkeep_conf = get_gkeep_config()

        # create canvas obj
        self.canv = Canvas(
            self.canvas_conf["api_url"],
            keyring.get_password('canvas-token', self.canvas_conf["api_username"])
        )

        # create todo obj (gkeep)
        self.todo = GKeep(self.gkeep_conf)

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
            # get updated canvas tasks
            canvas_tasks = get_assignments(
                self.courses, self.user, **self.app_conf["assignments_conf"]
            )

            # print assignments
            if self.app_conf["console_print"]:
                self.print_assignments(canvas_tasks)

            # get todo state
            todo_dict = self.todo.request_todo_state(self.app_conf["classes"])

            # generate dictionary of updates to todo state with assignments
            update_dict = self.gen_update_todo_dict(todo_dict, canvas_tasks)

            # set todo state
            self.todo.post_todo_state(update_dict, self.app_conf["classes"])

            # sleep for <update_rate> minutes
            sleep(self.app_conf["update_rate"])


    @staticmethod
    def print_assignments(asssignments: Dict[Course, List[Task]]):
        """Pretty prints assignments for each course

        Parameters
        ----------
        asssignments : Dict[Course, List[Task]]
            assignments to print
        """
        for course, course_assignments in asssignments.items():
            print(f"{fore.GREEN}{style.BOLD}{course.name}:{style.RESET}")

            # print each assignment
            for assmnt in course_assignments:
                print("  " + str(assmnt))

    @staticmethod
    def gen_update_todo_dict(
            todo_dict: Dict[int, List[Task]], canvas_tasks: Dict[Course, List[Task]]
    ) -> Dict[int, Dict[Update, List[Any]]]:
        """Generates update dictionary consisting of change to make to todo

        Parameters
        ----------
        todo_dict : Dict[int, List[Task]]
            todo dictionary, contains state from todo app, keyed by course id
        canvas_tasks : Dict[Course, List[Task]]
            tasks dictionary from canvas, keyed by Course object

        Returns
        -------
        Dict[int, Dict[Update, List[Any]]]
            update dictionary, keyed by course ID
        """
        # init update dict
        update_dict = collections.defaultdict(lambda: collections.defaultdict(list))

        # iterate over courses
        for course, course_canv_tasks in canvas_tasks.items():
            # get todo tasks for course
            todo_tasks = todo_dict[course.id]

            # iterate over canvas tasks
            for canv_task in course_canv_tasks:
                # check if task exists in todo tasks
                if not canv_task in todo_tasks:
                    # check if same task exists, but is marked incomplete in todo
                    if (
                            (canv_task.name, canv_task.due_date) in
                            [(t.name, t.due_date) for t in todo_tasks]
                    ):
                        # mark task as complete in todo if complete in canvas
                        if canv_task.completed == Completed.COMPLETE:
                            update_dict[course.id][Update.MARK_COMPLETE].append(canv_task)

                    else:
                        # if task does not exist at all in todo, add it
                        update_dict[course.id][Update.ADD].append(canv_task)

        # return update dict
        return update_dict
