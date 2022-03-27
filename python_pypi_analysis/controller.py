"""Main orchestrator."""
import requests

from python_pypi_analysis.models.package import Package
from python_pypi_analysis.utilities.database import (
    STATUS_COMPLETE,
    STATUS_FAILED,
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
        print("done")

    def _process_next_package(self):
        """Process a new package."""
        package = self._database.get_unprocessed_package()
        while package:
            try:
                self._fetch_package_pypi_data(package)
                package = self._database.get_unprocessed_package()
                self._database.set_package_status(
                    package=package, status=STATUS_COMPLETE
                )
            except Exception:
                self._database.set_package_status(package=package, status=STATUS_FAILED)
        self._done()

    def _fetch_package_pypi_data(self, package: Package):
        """Fetch paackage data on each package."""
        url: str = f"https://pypi.org/pypi/{package.package_name}/json"
        response = requests.get(url)
        response_json = response.json()
        package.project_urls = response_json.get("info", {}).get("project_urls", {})
        urls = response_json.get("urls", [])
        download_urls = {
            url_details["packagetype"]: url_details["url"] for url_details in urls
        }

        package.download_urls = download_urls
        package.version = response_json.get("info", {}).get("version", "0")
        self._database.update_package_pypi_data(package=package)
