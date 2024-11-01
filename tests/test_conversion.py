"""Module for testing the good conversion of the qmllint report to a CodeQuality report."""

import logging
import pytest

from qmllint_codequality import codequality, qmllint

logger = logging.getLogger(f"qmllint_codequality.{__name__}")

class TestRuleIsFound:
    """Check that a qmllint rule violation can be refound in the CodeQuality report."""

    @pytest.mark.parametrize("qmllint_rule", qmllint.Rules)
    def test_is_found(self, code_quality_report: list[codequality.Report], qmllint_rule: qmllint.Rules) -> None:
        """Check that all the rules can be found in a code_quality_report.

        The QML files regroups all the known rules violation. So if one rule is not found them, there is an error in the
        conversion (mostly use of the special value Rules.UNKNOWN).

        If ``qmllint_rule`` is Rules.UNKNOWN, them it's absence is a success.

        :param code_quality_report: The rule to found
        :type code_quality_report: list[codequality.Report]
        :param qmllint_rule: The rule to found
        :type qmllint_rule: qmllint.Rules
        """

        for report in code_quality_report:
            if qmllint_rule.value in report["check_name"]:
                logger.debug("Find rule violation of '%s' in file '%s'", qmllint_rule, report["location"]["path"])
                assert qmllint_rule is not qmllint.Rules.UNKNOWN
                break
        else:
            assert qmllint_rule is qmllint.Rules.UNKNOWN
