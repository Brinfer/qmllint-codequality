"""Module for testing the good conversion of the qmllint report to a CodeQuality report."""

import json
import tempfile

import pytest

import qmllint_codequality
from qmllint_codequality import codequality, qmllint
from tests import QMLLINT_REPORT, logger


class TestRuleIsFound:
    """Check that a qmllint rule violation can be refound in the CodeQuality report."""

    CODE_QUALITY_REPORT: list[codequality.Report]

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test suite.

        Convert the qmllint report to a CodeQuality JSON report.

        :raises RuntimeError: Failed to convert the qmllint report.
        """
        with tempfile.NamedTemporaryFile("a+") as codequality_report:
            logger.info("Convert the qmllint report to a CodeQuality report in %s", codequality_report.name)

            # If the returned value is less than 0, then an error occurred,
            # and at least one rule violation must be found
            if (nb_error := qmllint_codequality.convert_file(QMLLINT_REPORT, codequality_report.name)) < 1:
                raise RuntimeError("Failed to convert the qmllint report")

            logger.info("Find %d errors in the QML files", nb_error)

            # Load the JSON report resulting of the conversion

            # with open(TestRuleIsFound.CODE_QUALITY_REPORT_FILE,     "r", encoding="utf8") as json_report:
            TestRuleIsFound.CODE_QUALITY_REPORT = json.load(codequality_report)

    @pytest.mark.parametrize("qmllint_rule", qmllint.Rules)
    def test_is_found(self, qmllint_rule: qmllint.Rules) -> None:
        """Check that all the rules can be found in a CodeQualityReport.

        The QML files regroups all the known rules violation. So if one rule is not found them, there is an error in the
        conversion (mostly use of the special value Rules.UNKNOWN).

        If ``qmllint_rule`` is Rules.UNKNOWN, them it's absence is a success.

        :param qmllint_rule: The rule to found
        :type qmllint_rule: qmllint.Rules
        """

        for report in TestRuleIsFound.CODE_QUALITY_REPORT:
            if qmllint_rule.value in report["check_name"]:
                logger.debug("Find rule violation of '%s' in file '%s'", qmllint_rule, report["location"]["path"])
                assert qmllint_rule is not qmllint.Rules.UNKNOWN
                break
        else:
            assert qmllint_rule is qmllint.Rules.UNKNOWN
