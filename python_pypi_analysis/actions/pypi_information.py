"""Class to fetch information from pypi.org."""
from typing import Optional

import requests

from python_pypi_analysis.actions.task import Task
from python_pypi_analysis.models.package import Package
from python_pypi_analysis.utilities.database import (
    ACTION_COMPLETE,
    ACTION_ERROR,
    ACTION_IN_PROGRESS,
    ACTION_READY,
    Database,
)


class PypiInformation(Task):
    """This class is responsible for getting the information from pypi."""

    __slots__ = (
        "_database_handler",
        "_package",
    )

    def __init__(self, package: Package, database_handler: Database) -> None:
        """
        Initialise the PypiInformation object.

        Args:
            package: The package to analyse.
            database_handler: The database handler.
        """
        self._database_handler = database_handler
        self._package = package

    def run(self):
        """
        Run the analysis.

        Returns:
            The package with the information added.
        """
        url: str = f"https://pypi.org/pypi/{self._package.package_name}/json"
        response = requests.get(url)
        if response.status_code != 200:
            self._update_status(status=ACTION_ERROR)
            return
        response_json = response.json()
        self._package.project_urls = response_json.get("info", {}).get(
            "project_urls", {}
        )
        urls = response_json.get("urls", [])
        download_urls: list[dict[str, str]] = []
        for download_url in urls:
            download_url_dict = {
                "url": download_url.get("url"),
                "type": download_url.get("type"),
            }
            download_urls.append(download_url_dict)
        self._package.download_urls = download_urls
        self._package.version = response_json.get("info", {}).get("version", "0")
        self._add_download_urls(downloads=self._package.download_urls)
        self._add_project_urls(urls=self._package.project_urls)
        self._update_package_version(version=self._package.version)
        self._update_status(status=ACTION_COMPLETE)

    def _add_download_urls(self, downloads: list[dict[str, str]]):
        """
        Add URL's for package.

        Args
            urls: Dict of urls to add
        """
        add_sql = "INSERT INTO package_download_urls (name, url, for_package) VALUES (?, ?, ?)"
        for download in downloads:
            if download.get("type") is None:
                download["type"] = "unknown"
            add_parameters: tuple[str, str, int] = (
                download.get("type", ""),
                download.get("url", ""),
                self._package.database_id,
            )
            self._database_handler.execute_sql(sql=add_sql, parameters=add_parameters)
        self._database_handler.commit()

    def _add_project_urls(self, urls: dict[str, str] = None):
        """
        Add URL's for package.

        Args
            urls: Dict of urls to add
        """
        if not urls:
            return
        add_sql = "INSERT INTO package_urls (name, url, for_package) VALUES (?, ?, ?)"
        for url_type in urls:
            add_parameters: tuple[str, str, int] = (
                url_type,
                urls[url_type],
                self._package.database_id,
            )
            self._database_handler.execute_sql(sql=add_sql, parameters=add_parameters)
        self._database_handler.commit()

    def _update_package_version(self, version: str):
        """
        Update the package version in the database.

        Args:
            version: package version
        """
        update_sql = "UPDATE packages SET version = ? WHERE id = ?"
        update_parameters: tuple[str, int] = (
            version,
            self._package.database_id,
        )
        self._database_handler.execute_sql(sql=update_sql, parameters=update_parameters)
        self._database_handler.commit()

    def _update_status(self, status: int):
        """
        Update the status in the database.

        Args:
            status: The status to update to.
        """
        update_sql = "UPDATE packages SET pypi_info_status = ? WHERE id = ?"
        update_parameters: tuple[int, int] = (
            status,
            self._package.database_id,
        )
        self._database_handler.execute_sql(sql=update_sql, parameters=update_parameters)
        self._database_handler.commit()

    @classmethod
    def get_next_task(cls, database_handler: Database) -> Optional[Task]:
        """
        Get the next task to run.

        Returns:
            The next task to run.
        """
        fetch_sql = (
            "SELECT id, name FROM packages WHERE pypi_info_status = ? ORDER BY RAND();"
        )
        parameters: tuple[int] = (ACTION_READY,)
        res = database_handler.execute_sql(sql=fetch_sql, parameters=parameters)
        random_package_result = res.fetchone()
        task: Optional[Task] = None
        if random_package_result:
            package = Package(
                package_name=random_package_result[1],
                database_id=random_package_result[0],
            )
            update_sql = "UPDATE packages SET pypi_info_status = ? WHERE id = ?"
            update_parameters: tuple[int, int] = (
                ACTION_IN_PROGRESS,
                int(random_package_result[0]),
            )
            database_handler.execute_sql(sql=update_sql, parameters=update_parameters)
            database_handler.commit()
            task = PypiInformation(package=package, database_handler=database_handler)
        return task
