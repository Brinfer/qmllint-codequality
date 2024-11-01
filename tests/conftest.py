"""Module providing shared fixture for all the tests.

.. seealso::
    https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import json
import pathlib
import pytest
import qmllint_codequality
import tempfile

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


@pytest.fixture(scope="session")
def code_quality_report(qmllint_report: pathlib.Path) -> list[qmllint_codequality.codequality.Report]:
    """Fixture converting the qmllint report into a list of ``codequality.Report``.

    :param qmllint_report: Path to the qmllint report.
    :type qmllint_report: pathlib.Path
    :raises RuntimeError: Failed to convert the qmllint report.
    :return: The list of qmllint error converter into ``codequality.Report``.
    :rtype: list[codequality.Report]
    """
    with tempfile.NamedTemporaryFile("a+") as codequality_report:
        logger.info("Convert the qmllint report to a CodeQuality report in '%s'", codequality_report.name)

        # If the returned value is less than 0, then an error occurred,
        # at least one rule violation must be found
        if (nb_error := qmllint_codequality.convert_file(qmllint_report, codequality_report.name)) < 1:
            raise RuntimeError("Failed to convert the qmllint report")

        logger.info("Find %d errors in the QML files", nb_error)

        # Load the JSON report resulting of the conversion
        return json.load(codequality_report)
