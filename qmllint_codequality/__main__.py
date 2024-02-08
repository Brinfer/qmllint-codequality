"""CLI app for converting qmllint JSON report to Code Quality JSON report."""

import argparse
import logging
import sys

from qmllint_codequality import VERSION_MESSAGE, __project__, convert_file


def _get_args() -> argparse.Namespace:
    """Parse the command line option passed to the application.

    :return: The parsed options
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, prog=__project__, description=__doc__
    )

    parser.add_argument(
        "input_file",
        help="The path to the qmllint JSON output to be converted",
        type=str,
        action="store",
    )

    parser.add_argument(
        "output_file",
        help="output filename to write JSON to (default: %(default)s)",
        type=str,
        default="clang-tidy.json",
        action="store",
    )

    parser.add_argument(
        "-V",
        "--version",
        help=f"print the {__project__} version and exit",
        action="version",
        version=VERSION_MESSAGE,
    )

    parser.add_argument(
        "-v",
        "--verbosity",
        choices=[
            logging.getLevelName(logging.WARNING),
            logging.getLevelName(logging.INFO),
            logging.getLevelName(logging.DEBUG),
        ],
        help="indicates the level of verbosity",
        type=str,
        default=logging.getLevelName(logging.INFO),
    )

    # Parse the arguments
    return parser.parse_args()


def _configure_log(login_level: str) -> None:
    """Configure the logging library the to given level.

    :param login_level: The login level.
    :type login_level: str
    """
    logging.basicConfig(
        level=logging.getLevelName(login_level),
        format="%(asctime)s %(levelname)s : %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> int:
    """Convert a qmllint JSON output to Code Climate JSON file, at the command line.

    :return:  0 if successful, 0 otherwise.
    :rtype: int
    """
    if sys.version_info < (3, 10, 0):
        sys.stderr.write("You need python 3.10 or later to run this script\n")
        return 1

    args = _get_args()

    _configure_log(args.verbosity)

    # Convert the clang-tidy output to JSON here.
    ret = convert_file(args.input_file, args.output_file)
    if ret < 0:
        logging.error("Conversion failed")
        return 1

    # # Logging the total count.
    logging.info("Converted %d qmllint issues", ret)

    return 0


if __name__ == "__main__":
    sys.exit(main())
