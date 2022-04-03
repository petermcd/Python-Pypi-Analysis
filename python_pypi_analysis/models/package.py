"""Model for pypi packages."""
from python_pypi_analysis.models.file import File


class Package:
    """Model for pypi package."""

    __slots__ = [
        "_id",
        "_database_id",
        "_downloads",
        "_package_name",
        "_project_urls",
        "_download_urls",
        "_analysed_version",
        "_files",
    ]

    def __init__(self, package_name: str, downloads: int = 0, database_id: int = 0):
        """Initialize Package."""
        self._id: int = database_id
        self._downloads: int = downloads
        self._package_name: str = package_name
        self._project_urls: dict[str, str] = {}
        self._download_urls: list[dict[str, str]] = []
        self._analysed_version: str = "0"
        self._files: dict[str, File] = {}

    @property
    def database_id(self) -> int:
        """
        Property for database ID.

        Returns:
            Database ID
        """
        return self._id

    @database_id.setter
    def database_id(self, database_id: int):
        """
        Setter for database ID.

        Args:
            database_id: Database ID
        """
        self._id = database_id

    @property
    def downloads(self) -> int:
        """
        Property for download count for the package.

        Returns:
            package download count as an int
        """
        return self._downloads

    @property
    def package_name(self) -> str:
        """
        Property for package name.

        Returns:
            package name as a string
        """
        return self._package_name

    @property
    def project_urls(self) -> dict[str, str]:
        """
        Property for project URLs.

        Returns:
            Dictionary of project URL's
        """
        return self._project_urls

    @project_urls.setter
    def project_urls(self, urls: dict[str, str]):
        """
        Setter for project URLS.

        Args:
            urls: Dictionary of project urls
        """
        self._project_urls = urls

    @property
    def download_urls(self) -> list[dict[str, str]]:
        """
        Property for download URLs.

        Returns:
            Dictionary of download URL's
        """
        return self._download_urls

    @download_urls.setter
    def download_urls(self, urls: list[dict[str, str]]):
        """
        Setter for download URLS.

        Args:
            urls: List of download urls
        """
        self._download_urls = urls

    @property
    def version(self) -> str:
        """
        Property for version.

        Returns:
            Version
        """
        return self._analysed_version

    @version.setter
    def version(self, version: str):
        """
        Setter for version.

        Args:
            version: version
        """
        self._analysed_version = version

    def get_file(self, name: str) -> File:
        """
        Fetch the file object for the given file.

        Args:
            name: name of instance required

        Returns:
            Instance of File of the given name
        """
        if name not in self._files.keys():
            self._files[name] = File(package=self, name=name)
        return self._files[name]
