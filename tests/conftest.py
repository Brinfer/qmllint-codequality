"""Module providing shared fixture for all the tests.

.. seealso::
    https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os

from tests import QMLLINT_REPORT, get_all_qml_file, logger, run_qmllint


def pytest_sessionstart() -> None:
    """Function called before performing collection and entering the run test loop.

    This session setup function ensure that an up to date JSON report is generated before each test session.

    :raises RuntimeError: Failed to set up the test session.
    """
    logger.info("Setting up the tests session")

    # Ensure that that reports dir exist
    os.makedirs(os.path.dirname(QMLLINT_REPORT), exist_ok=True)

    try:
        run_qmllint(QMLLINT_REPORT, get_all_qml_file())
    except Exception as e:
        raise RuntimeError("Setup of the test session failed") from e
