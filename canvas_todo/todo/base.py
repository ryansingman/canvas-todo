from abc import ABC, abstractmethod


class TodoBase(ABC):
    """Todo base class
    """
    @abstractmethod
    def request_todo_state(self):
        """Requests state from API and updates local todo state
        """
        pass

    @abstractmethod
    def post_todo_state(self):
        """Posts state to API to match with new changes
        """
        pass

    @property
    def todo_state(self):
        """Returns state of todo app
        """
        pass