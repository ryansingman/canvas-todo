from typing import Dict, List
from datetime import datetime, timezone

from canvasapi.course import Course
from canvasapi.assignment import Assignment

def get_assignments(
        courses: List[Course],
        **kwargs: Dict
) -> Dict[Course, List[Assignment]]:
    """Returns dictionary of assignments for each course, sorted by due date

    Parameters
    ----------
    courses : List[Course]
        list of course objects
    **kwargs : Dict
        keywords dict to pass to filter function

    Returns
    -------
    Dict[Course, List[Assignment]]
        dict of assignments for each course
    """
    return {
        course: sorted(
            [
                a
                for a in course.get_assignments()
                if should_include(a, **kwargs)
            ], key=lambda x: datetime.fromisoformat(x.due_at)
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
            datetime.fromisoformat(assmnt.due_at) - datetime.now(timezone.utc)
        ).days < due_date_horizon
    )
