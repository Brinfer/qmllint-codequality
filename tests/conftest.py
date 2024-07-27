"""Module providing shared fixture for all the tests.

.. seealso::
    https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import pytest
import pathlib

from tests import get_all_qml_file, logger, run_qmllint


@pytest.fixture(scope="session")
def qmllint_report(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Execute qmllint on all QML files.

    The report is stored in a temporary file.

    :param tmp_path_factory: A temporary path factory.
    :type tmp_path_factory: pytest.TempPathFactory
    :return: The path to the qmllint report.
    :rtype: str

    .. seealso::
       - ``tests.get_all_qml_file``
       - ``tests.run_qmllint``
    """
    report = tmp_path_factory.mktemp("report").joinpath("qmllint_report.json")

    run_qmllint(report, get_all_qml_file())

    logger.debug("qmllint report file written in '%s'", report)
    return report
