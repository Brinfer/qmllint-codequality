"""Top level module for qmllint-codequality package."""

import logging
import os
import re
import pathlib
import shutil
import subprocess
import sys
from packaging.version import Version, InvalidVersion

sys.path.append("../qmllint_codequality")  # Add the package to the sys path

logger = logging.getLogger("qmllint_codequality.test")

QML_DIR = pathlib.Path(pathlib.Path(__file__).parent, "qml")
"""Path to the directory containing all the QML files."""

__REGEX_CAPTURE_VERSION = re.compile(r"(\d+\.\d+)\.?")
"""Regex used to capture the version of qmllint.

Capture only the major and the minor value of the version, ignore the patch part.
"""

__QMLLINT_MINIMAL_VERSION = Version("6.4.0")
"""Minimal version of qmllint supported."""


def get_all_qml_file() -> list[pathlib.PurePath]:
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
                qml_files.append(pathlib.PurePath(dirpath, filename))
                logger.debug("Find QML file '%s'", qml_files[-1])

    logger.info("Find %d QML files", len(qml_files))
    return qml_files


def run_qmllint(report_file: pathlib.Path, qml_files: list[pathlib.PurePath]) -> None:
    """Execute the qmllint command line.

    Remove the previous ``report_file`` if exist.

    :param report_file: The qmllint JSON report to generate.
    :type report_file: str
    :param qml_files: The list of QML file.
    :type qml_files: list[str]
    :raises ExecError: Failed to find the command ``qmllint``
    :raises InvalidVersion: Current version of qmllint is not supported
    :raises FileNotFoundError: Failed to generate the ``report_file``
    """
    # Ensure that qmllint is installed
    if shutil.which("qmllint"):
        # Ensure that the qmllint version is correct
        with subprocess.Popen("qmllint --version", stdout=subprocess.PIPE, shell=True, text=True) as qmllint_version:
            qmllint_version.wait()
            assert qmllint_version.stdout

            if version_match := __REGEX_CAPTURE_VERSION.search(qmllint_version.stdout.read()):
                version = Version(version_match.group(1))
                logger.info("Current version of qmllint: '%s'", version)

                if version < __QMLLINT_MINIMAL_VERSION:
                    raise InvalidVersion(f"Minimal version requirement not fulfilled (>={__QMLLINT_MINIMAL_VERSION})")
            else:
                logger.warning("qmllint's version not found. Continue anyway ...")
    else:
        raise shutil.ExecError("qmllint not found")

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
    if not report_file.is_file():
        raise FileNotFoundError(f"'{report_file}' has not been generated")
