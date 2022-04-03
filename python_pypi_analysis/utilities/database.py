"""Class to handle database interactions."""
from typing import Optional

import mariadb

from python_pypi_analysis.models.package import Package
from python_pypi_analysis.utilities.configuration import Configuration

STATUS_READY = 0
STATUS_IN_PROGRESS = 1
STATUS_FAILED = 2
STATUS_PYPI_COMPLETE = 3
STATUS_CODE_ANALYSIS_IN_PROGRESS = 4
STATUS_CODE_ANALYSIS_FAILED = 4
STATUS_CODE_ANALYSIS_COMPLETE = 6


class Database:
    """Class to handle database interaction."""

    __slots__ = [
        "_commit_required",
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
        self._commit_required: bool = False
        if not configuration:
            configuration = Configuration()
        self._configuration: Configuration = configuration
        self._create_connection()

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

    def get_unprocessed_package(self) -> Optional[Package]:
        """
        Retrieve a random unprocessed package from the database.

        Returns:
            Random unprocessed package or None if all processed
        """
        sql = "SELECT id, name FROM packages WHERE status = 0 ORDER BY RAND();"
        self._cursor.execute(sql)
        random_package_result = self._cursor.fetchone()
        package: Optional[Package] = None
        if random_package_result:
            package = Package(
                package_name=random_package_result[1],
                database_id=random_package_result[0],
            )
            self.set_package_status(package=package, status=STATUS_IN_PROGRESS)
        return package

    def execute(self, sql: str, parameters: Optional[set], commit: bool = True):
        """
        Process SQL statement.

        Args:
            sql: SQL statement to be processed
            parameters: Parameters for query
            commit: True if a commit should immediately occur

        Returns:
            Cursor for the query
        """
        self._cursor.execute(sql, paramets=parameters)
        if commit:
            self._connection.commit()
        return self._cursor

    def set_package_status(self, package: Package, status: int):
        """
        Set te package status.

        Args:
            package: Package to be updated
            status: Status ID to set
        """
        sql = "UPDATE packages SET status = ? WHERE name = ?;"
        self._cursor.execute(sql, (status, package.package_name))
        self._commit_required = False
        self._connection.commit()

    def update_package_pypi_data(self, package: Package):
        """
        Update given package in the database.

        Args:
            package: Package to be updated
        """
        update_package_sql = "UPDATE packages SET version = ? WHERE id = ?"
        self._cursor.execute(update_package_sql, (package.version, package.database_id))

        insert_package_download_sql = "INSERT INTO package_download_urls (name, url, for_package) VALUES (?, ?, ?);"
        for download_details in package.download_urls:
            self._cursor.execute(
                insert_package_download_sql,
                (
                    download_details["type"],
                    download_details["url"],
                    package.database_id,
                ),
            )

        insert_package_url_sql = (
            "INSERT INTO package_urls (name, url, for_package) VALUES (?, ?, ?);"
        )
        for url_name, url in package.project_urls.items():
            self._cursor.execute(
                insert_package_url_sql, (url_name, url, package.database_id)
            )

        self._connection.commit()
        self._commit_required = False

    def close(self):
        """Close the database connection."""
        if self._commit_required:
            self._connection.commit()
        self._connection.close()
