from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .task import Task
from .update import Update


class TodoBase(ABC):
    """Todo base class
    """
    @abstractmethod
    def request_todo_state(self, courses: Dict[int, Any]) -> Dict[int, List[Task]]:
        """Requests state from API and updates local todo state

        Parameters
        ----------
        courses : Dict[int, Any]
            courses dictionary (keyed by course ID)

        Returns
        -------
        Dict[int, List[Task]]
            todo dictionary (keyed by course ID)
        """
        pass

    @abstractmethod
    def post_todo_state(self, update_dict: Dict[int, Dict[Update, Any]], courses: Dict[int, Any]):
        """Posts state to API to match with new changes

        Parameters
        ----------
        update_dict : Dict[int, Dict[Update, List[Any]]]
            update dictionary (keyed by course ID)
        courses : Dict[int, Any]
            courses dictionary (keyed by course ID)
        """
        pass

    @property
    def todo_state(self):
        """Returns state of todo app
        """
        pass