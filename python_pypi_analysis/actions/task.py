"""Abstract class for tasks."""
from abc import ABC, abstractmethod

from python_pypi_analysis.models.package import Package
from python_pypi_analysis.utilities.database import Database


class Task(ABC):
    """Abstract class for tasks."""

    @abstractmethod
    def __init__(self, database_handler: Database) -> None:
        """Abstract."""
        pass

    @abstractmethod
    def run(self) -> Package:
        """Abstract."""
        pass
