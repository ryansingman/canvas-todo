import re
from dataclasses import dataclass
from datetime import datetime

from gkeepapi.node import ListItem
from canvasapi.assignment import Assignment
from canvasapi.user import User

from ..utils import time_utils
from .completed import Completed


@dataclass
class Task:
    """Task data class"""
    name: str
    due_date: datetime
    completed: Completed

    @staticmethod
    def from_gkeep_task(keep_task: ListItem):
        """Builds task from google keep task

        Parameters
        ----------
        keep_task : ListItem
            google keep task to build Task from

        Returns
        -------
        Task
            task data object built from google keep task
        """
        # parse task text
        name, date_str = re.match(r"^(.*) \((.*)\)$", keep_task.text).groups()

        # build task object
        return Task(
            name,
            time_utils.from_due_date_str(date_str),
            Completed.COMPLETE if keep_task.checked else Completed.INCOMPLETE
        )

    @staticmethod
    def from_canvas_assmnt(canvas_assmnt: Assignment, user: User):
        """Builds task from canvas assignment

        Parameters
        ----------
        canvas_assmnt : Assignment
            canvas assignment to build Task from
        user : User
            user to use to get completed-ness

        Returns
        -------
        Task
            task data object built from canvas assignment
        """
        # get completedness of assignment
        if canvas_assmnt.submission_types == ['none']:
            completed = Completed.UNKNOWN
        elif not canvas_assmnt.get_submission(user).submitted_at is None:
            completed = Completed.COMPLETE
        else:
            completed = Completed.INCOMPLETE

        return Task(
            canvas_assmnt.name,
            time_utils.from_iso8601(canvas_assmnt.due_at),
            completed
        )

    def __str__(self) -> str:
        """Returns string representation of task

        Returns
        -------
        str
            string repr of task
        """
        # return formatted task string
        return f"[{str(self.completed)}] {time_utils.to_due_date_str(self.due_date):^16}: {self.name:<80}"

    def todo_str(self) -> str:
        """Returns string representation of task, used by todo app

        Returns
        -------
        str
            string repr of task
        """
        # return formatted assignment string
        return f"{self.name} ({time_utils.to_due_date_str(self.due_date)})"
