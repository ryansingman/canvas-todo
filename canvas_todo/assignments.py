from typing import Dict, List

from canvasapi.course import Course
from canvasapi.assignment import Assignment

def get_assignments(courses: List[Course]) -> Dict[Course, List[Assignment]]:
    """Returns dictionary of assignments for each course

    Parameters
    ----------
    courses : List[Course]
        list of course objects

    Returns
    -------
    Dict[Course, List[Assignment]]
        dict of assignments for each course
    """
    return {
        course: [a for a in course.get_assignments()]
        for course in courses
    }
