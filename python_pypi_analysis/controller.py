"""Main orchestrator."""
from random import randint
from time import sleep
from typing import Optional

from python_pypi_analysis.actions.pypi_information import PypiInformation
from python_pypi_analysis.actions.task import Task
from python_pypi_analysis.utilities.database import Database


class Controller:
    """Main orchestrator for the system."""

    __slots__ = [
        "_database",
    ]

    def __init__(self):
        """Initialize Controller."""
        self._database = Database()

    def run(self):
        """Run."""
        has_task, task = self._next_task()
        while has_task:
            task.run()
            has_task, task = self._next_task()
            sleep(randint(5, 10))
        self._done()

    def _done(self):
        """Close database."""
        self._database.close()

    def _next_task(self) -> tuple[bool, Optional[Task]]:
        """Pick a task."""
        task = PypiInformation.get_next_task(self._database)
        has_task = task is not None
        return has_task, task
