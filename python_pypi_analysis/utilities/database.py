"""Class to handle database interactions."""
from typing import Optional, Union

import mariadb

from python_pypi_analysis.utilities.configuration import Configuration

ACTION_READY: int = 0
ACTION_IN_PROGRESS: int = 1
ACTION_ERROR: int = 2
ACTION_COMPLETE: int = 3


class Database:
    """Class to handle database interaction."""

    __slots__ = [
        "_configuration",
        "_connection",
        "_cursor",
    ]

    def __init__(self, configuration: Optional[Configuration] = None):
        """
        Initialize Database.

        Args:
            configuration: Instance of Configuration, if None a new copy is instantiated
        """
        if not configuration:
            configuration = Configuration()
        self._configuration: Configuration = configuration
        self._create_connection()

    def execute_sql(
        self,
        sql: str,
        parameters: Optional[tuple[Union[int, str], ...]],
        commit: bool = False,
    ):
        """
        Process SQL statement.

        Args:
            sql: SQL statement to be processed
            parameters: Arguments for query
            commit: True if a commit should immediately occur

        Returns:
            Cursor for the query
        """
        self._cursor.execute(sql, parameters)
        if commit:
            self._connection.commit()
        return self._cursor

    def _create_connection(self):
        """Create a database connection."""
        self._connection = mariadb.connect(
            user=self._configuration.database_username,
            password=self._configuration.database_password,
            host=self._configuration.database_host,
            port=self._configuration.database_port,
            database=self._configuration.database_name,
        )
        self._cursor = self._connection.cursor()

    def commit(self):
        """Commit changes to the database."""
        self._connection.commit()

    def close(self):
        """Close the database connection."""
        self.commit()
        self._connection.close()
