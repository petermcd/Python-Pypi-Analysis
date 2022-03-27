"""Main runner script."""
from python_pypi_analysis.controller import Controller


def run():
    """Initiate process."""
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    run()
