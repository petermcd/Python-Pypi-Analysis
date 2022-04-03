"""Main orchestrator."""
import os
import tempfile
from os.path import sep
from random import randint
from time import sleep

import requests

from python_pypi_analysis.models.package import Package
from python_pypi_analysis.utilities.database import (
    STATUS_FAILED,
    STATUS_PYPI_COMPLETE,
    Database,
)


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
        self._process_next_package()

    def _done(self):
        """Close database."""
        self._database.close()

    def _process_next_package(self):
        """Process a new package."""
        package = self._database.get_unprocessed_package()
        try:
            self._fetch_package_pypi_data(package)
            self._database.set_package_status(
                package=package, status=STATUS_PYPI_COMPLETE
            )
        except Exception:
            self._database.set_package_status(package=package, status=STATUS_FAILED)
        self._done()
        sleep(randint(5, 10))

    def _identify_bug_count(self, package: Package):
        """
        Identify the number of bugs in the given package.

        Args:
            package: Package to analyse
        """
        # TODO analyse bugs

    def _analyse_code_complexity(self, package: Package):
        """
        Download and analyse the code complexity of the given package.

        Args:
            package: Package to analyse
        """
        # path = self._download_and_extract(package=package)
        # TODO extract the code
        # TODO analyse the code
        self._cleanup(package=package)

    def _analyse_code(self, package: Package):
        """
        Analyse the complexity of the code.

        Args:
            package: Package to be analysed.
        """

    def _download_and_extract(self, package: Package) -> str:
        """
        Download and extract a pypi package.

        Args:
            package: Package to be downloaded

        Returns:
            Path to the extracted source code
        """
        url = ""
        response = requests.get(url)
        source_path = f"{tempfile.gettempdir()}{sep}{package.package_name}"
        archive_path = f"{source_path}"  # TODO add extension
        with open(archive_path, "wb") as handler:
            handler.write(response.content)
        # TODO extract the content using unzip
        # shutil.unpack_archive
        return source_path

    def _cleanup(self, package: Package):
        """
        Clean up package files.

        Args:
            package: Package to be cleaned
        """
        source_path = f"{tempfile.gettempdir()}{sep}{package.package_name}"
        archive_path = f"{source_path}"  # TODO add extension
        if os.path.exists(source_path):
            os.remove(source_path)
        if os.path.exists(archive_path):
            os.remove(archive_path)

    def _fetch_package_pypi_data(self, package: Package):
        """Fetch paackage data on each package."""
        url: str = f"https://pypi.org/pypi/{package.package_name}/json"
        response = requests.get(url)
        response_json = response.json()
        package.project_urls = response_json.get("info", {}).get("project_urls", {})
        urls = response_json.get("urls", [])
        download_urls: list[dict[str, str]] = []
        for download_url in urls:
            download_url_dict = {
                "url": download_url.get("url"),
                "type": download_url.get("packagetype"),
            }
            download_urls.append(download_url_dict)
        package.download_urls = download_urls
        package.version = response_json.get("info", {}).get("version", "0")
        self._database.update_package_pypi_data(package=package)
