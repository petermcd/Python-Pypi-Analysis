"""File class."""


class File:
    """File class."""

    __slots__ = [
        "_blank_lines",
        "_comment_lines",
        "_lines_of_code",
        "_multi_line_comment_lines",
        "_name",
        "_package",
        "_source_lines_of_code",
    ]

    def __init__(self, package, name: str):
        """
        Initialize File.

        Args:
            package: The package the file is a part of
            name: Name of the file
        """
        self._blank_lines: int = 0
        self._comment_lines: int = 0
        self._lines_of_code: int = 0
        self._multi_line_comment_lines: int = 0
        self._name: str = name
        self._package = package
        self._source_lines_of_code: int = 0

    @property
    def blank_lines(self):
        """
        Property for blank Lines.

        Returns:
            The number of blank lines
        """
        return self._blank_lines

    @blank_lines.setter
    def blank_lines(self, blank_lines: int):
        """
        Setter for blank lines.

        Args:
            blank_lines: The number of blank lines
        """
        self._blank_lines = blank_lines

    @property
    def comment_lines(self):
        """
        Property for Comment Lines.

        Returns:
            The number of comment lines
        """
        return self._comment_lines

    @comment_lines.setter
    def comment_lines(self, comment_lines: int):
        """
        Setter for comment lines.

        Args:
            comment_lines: The number of comment lines
        """
        self._comment_lines = comment_lines

    @property
    def lines_of_code(self):
        """
        Property for Lines Of Code.

        Returns:
            The number of lines of code
        """
        return self._lines_of_code

    @lines_of_code.setter
    def lines_of_code(self, lines_of_code: int):
        """
        Setter for Lines Of Code.

        Args:
            lines_of_code: The number of lines of code
        """
        self._lines_of_code = lines_of_code

    @property
    def multi_line_comment_lines(self):
        """
        Property for Multi Comment Lines.

        Returns:
            The number of multi comment lines
        """
        return self._multi_line_comment_lines

    @multi_line_comment_lines.setter
    def multi_line_comment_lines(self, multi_line_comment_lines: int):
        """
        Setter for multi comment lines.

        Args:
            multi_line_comment_lines: The number of multi comment lines
        """
        self._multi_line_comment_lines = multi_line_comment_lines

    @property
    def source_lines_of_code(self):
        """
        Property for Source Lines Of Code.

        Returns:
            The number of source lines of code
        """
        return self._source_lines_of_code

    @source_lines_of_code.setter
    def source_lines_of_code(self, source_lines_of_code: int):
        """
        Setter for Source Lines Of Code.

        Args:
            source_lines_of_code: The number of source lines of code
        """
        self._source_lines_of_code = source_lines_of_code
