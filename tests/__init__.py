"""Top level module for qmllint-codequality package."""

import logging
import os
import subprocess
import sys
import tempfile

sys.path.append("../qmllint_codequality")  # Add the package to the sys path


logger = logging.getLogger("qmllint_codequality.test")

QML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qml")
QMLLINT_REPORT = tempfile.NamedTemporaryFile("a+").name  # pylint: disable=consider-using-with


def get_all_qml_file() -> list[str]:
    """Get the absolute path of all the QML files.

    Search recursively the QML file in the QML_DIR folder.

    :return: The list of QML files.
    :rtype: list[str]
    """

    logger.info("Research all the QML files in %s", QML_DIR)
    qml_files = []

    for dirpath, _, filenames in os.walk(QML_DIR):
        for filename in filenames:
            if filename.endswith(".qml"):
                qml_files.append(os.path.join(dirpath, filename))
                logger.debug("Find QML file '%s'", qml_files[-1])

    logger.info("Find %d QML files", len(qml_files))
    return qml_files


def run_qmllint(report_file: str, qml_files: list[str]) -> None:
    """Execute the qmllint command line.

    Remove the previous ``report_file`` if exist.

    :param report_file: The qmllint JSON report to generate.
    :type report_file: str
    :param qml_files: The list of QML file.
    :type qml_files: list[str]
    :raises FileNotFoundError: Failed to generate the ``report_file``
    """
    logger.info("Run the qmllint tool, and save result in %s", report_file)

    subprocess.run(
        " ".join(
            [
                "qmllint",
                "--dry-run",
                f"--json '{report_file}'",
                "--alias warning",
                "--compiler warning",
                "--controls-sanity warning",
                "--deferred-property-id warning",
                "--deprecated warning",
                "--import warning",
                "--inheritance-cycle warning",
                "--multiline-strings warning",
                "--multiple-attached-objects warning",
                "--property warning",
                "--required warning",
                "--signal warning",
                "--type warning",
                "--unqualified warning",
                "--unused-imports warning",
                "--with warning",
                *[f"'{file}'" for file in qml_files],
            ]
        ),
        check=False,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Ensure that the report has been generated
    if not os.path.isfile(report_file):
        raise FileNotFoundError(f"'{report_file}' has not been generated")
