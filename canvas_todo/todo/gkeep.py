from datetime import datetime
from typing import Any, Dict, List

import keyring
import gkeepapi

from .base import TodoBase
from .task import Task
from .update import Update
from .completed import Completed
from ..utils import time_utils


class GKeep(TodoBase):
    """Google Keep class, used to interface with Google Keep
    """
    notes: Dict[str, List[Task]]
    conf: Dict

    def __init__(self, gkeep_conf: Dict):
        """Initialize google keep object

        Parameters
        ----------
        gkeep_conf : Dict
            google keep configuration
        """
        # set conf
        self.conf = gkeep_conf

        # set up google keep object
        self.keep = gkeepapi.Keep()
        self.keep.resume(
            gkeep_conf["api_username"],
            keyring.get_password("gkeep-key", gkeep_conf["api_username"])
        )

        # sync notes
        self.keep.sync()

    def post_todo_state(self, update_dict: Dict[int, Dict[Update, Any]], courses: Dict[int, Any]):
        """Posts state to API to match with new changes

        Parameters
        ----------
        update_dict : Dict[int, Dict[Update, List[Any]]]
            update dictionary (keyed by course ID)
        courses : Dict[int, Any]
            courses dictionary (keyed by course ID)
        """
        # iterate over courses
        for course, course_params in courses.items():
            # add course todo list if doesn't already exist
            if len(course_note_list := list(self.keep.find(course_params["nickname"]))) == 0:
                course_note = self.keep.createList(course_params["nickname"])
                course_note.color = course_params["color"]

            else:
                course_note = course_note_list[0]

            # ensure note is pinned/unpinned
            course_note.pinned = self.conf["pin_notes"]

            # add course tasks that are missing
            for task_to_add in update_dict[course][Update.ADD]:
                course_note.add(
                    task_to_add.todo_str(),
                    task_to_add.completed == Completed.COMPLETE
                )

            # mark newly completed tasks as complete
            for task_to_complete in update_dict[course][Update.MARK_COMPLETE]:
                task_idx = [
                    task.text
                    for task in course_note.items
                ].index(task_to_complete.todo_str())

                course_note.items[task_idx].checked = True

            # sort tasks by due date
            course_note.sort_items(
                key=self.key_func
            )

        # sync updates to google drive
        self.keep.sync()


    @staticmethod
    def key_func(task_str: str) -> datetime:
        """Returns datetime object given task string

        Parameters
        ----------
        task_str : str
            task string to generate key from

        Returns
        -------
        datetime
            datetime object generated from task string
        """
        task = Task.from_gkeep_task(task_str)

        # return max time if due date doesn't exist (goes to end of list)
        if task.due_date is None:
            return time_utils.max_time()

        else:
            return task.due_date

    def request_todo_state(self, courses: Dict[int, Any]) -> Dict[int, List[Task]]:
        """Requests and returns todo state from Google Keep API

        Parameters
        ----------
        courses : Dict[int, Any]
            courses dictionary (keyed by course ID)

        Returns
        -------
        Dict[int, List[Task]]
            todo dictionary (keyed by course ID)
        """
        # init todo dictionary
        todo_dict = {}

        # build tasks list for each course
        for course, course_params in courses.items():
            course_todo_list = list(self.keep.find(course_params["nickname"]))

            # if course list already exists
            if len(course_todo_list) > 0:
                todo_dict[course] = [
                    Task.from_gkeep_task(keep_task)
                    for keep_task in course_todo_list[0].items
                ]

            # if the course list doesn't exist, create one
            else:
                todo_dict[course] = []

        # return todo dictionary
        return todo_dict
