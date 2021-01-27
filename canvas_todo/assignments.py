from typing import Dict, List
from datetime import datetime, timezone

from canvasapi.course import Course
from canvasapi.assignment import Assignment
from canvasapi.user import User

from .utils import time_utils
from .todo.task import Task


def get_assignments(
        courses: List[Course],
        user: User,
        **kwargs: Dict
) -> Dict[Course, List[Task]]:
    """Returns dictionary of tasks for each course, sorted by due date

    Parameters
    ----------
    courses : List[Course]
        list of course objects
    user : User
        user to use to get completed-ness
    **kwargs : Dict
        keywords dict to pass to filter function

    Returns
    -------
    Dict[Course, List[Task]]
        dict of tasks for each course
    """
    return {
        course: sorted(
            [
                Task.from_canvas_assmnt(a, user)
                for a in course.get_assignments()
                if should_include(a, **kwargs)
            ], key=lambda x: x.due_date
        )
        for course in courses
    }


def should_include(assmnt: Assignment, due_date_horizon: int) -> bool:
    """Returns true if assignment meets supplied criteria

    Parameters
    ----------
    assmnt : Assignment
        assignment to check if meet criteria
    due_date_horizon : int
        maximum number of days from current date to due date

    Returns
    -------
    bool
        true if should include assignment
    """
    return (
        (
            time_utils.from_iso8601(assmnt.due_at) - datetime.now(timezone.utc)
        ).days < due_date_horizon
    )
