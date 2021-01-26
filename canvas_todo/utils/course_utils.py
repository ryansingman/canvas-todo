from typing import List

from canvasapi import Canvas
from canvasapi.course import Course


def get_courses_from_ids(canv: Canvas, ids: List[int]) -> List[Course]:
    """Gets canvas courses from canvas object, list of ids

    Parameters
    ----------
    canv : Canvas
        canvas object to get course from
    ids : List[int]
        list of course IDs

    Returns
    -------
    List[Course]
        list of course objects matching the course IDs
    """
    return [
        course
        for course in canv.get_courses()
        if course.id in ids
    ]
