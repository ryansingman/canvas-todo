from typing import Dict

import keyring
import gkeepapi

from .base import TodoBase


class GKeep(TodoBase):
    """Google Keep class, used to interface with Google Keep
    """
    def __init__(self, gkeep_conf: Dict):
        """Initialize google keep object

        Parameters
        ----------
        gkeep_conf : Dict
            google keep configuration
        """
        # set up google keep object
        keep = gkeepapi.Keep()
        keep.resume(
            gkeep_conf["api_username"],
            keyring.get_password("gkeep-key", gkeep_conf["api_username"])
        )

        # sync notes
        keep.sync()

    def post_todo_state(self):
        pass

    def request_todo_state(self):
        pass