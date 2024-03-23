"""Module providing a collection of class representing a qmllint report.

It's mostly TypedDict.
It facilitate dictionary/JSON manipulation, representing a report in qmllint format.
"""

from enum import Enum, unique
from typing import TypedDict

# https://codebrowser.dev/qt6/qtdeclarative/src/qmlcompiler/qqmljslogger.cpp.html#_ZN12QQmlJSLogger17defaultCategoriesEv
_QMLLINT_WARNING_SPLITTED: dict[str, dict] = {
    "RequiredProperty": {"desc": "Warn about required properties"},
    "PropertyAliasCycles": {"desc": "Warn about alias cycles or unresolved aliases"},
    "ImportFailure": {"desc": "Warn about failing imports and deprecated qmltypes"},
    "WithStatement": {
        "desc": "Warn about with statements as they can cause false positives when checking for unqualified access"
    },
    "InheritanceCycle": {"desc": "Warn about inheritance cycles"},
    "Deprecated": {"desc": "Warn about deprecated properties and types"},
    "BadSignalHandlerParameters": {"desc": "Warn about bad signal handler parameters"},
    "MissingType": {"desc": "Warn about missing types"},
    "UnresolvedType": {"desc": "Warn about unresolved types"},
    "RestrictedType": {"desc": "Warn about restricted types"},
    "PrefixedImportType": {"desc": "Warn about prefixed import types"},
    "IncompatibleType": {"desc": "Warn about missing types"},
    "MissingProperty": {"desc": "Warn about missing properties"},
    "NonListProperty": {"desc": "Warn about non-list properties"},
    "ReadOnlyProperty": {"desc": "Warn about writing to read-only properties"},
    "DuplicatePropertyBinding": {"desc": "Warn about duplicate property bindings"},
    "DuplicatedName": {"desc": "Warn about duplicated property/signal names"},
    "DeferredPropertyId": {"desc": "Warn about making deferred properties immediate by giving them an id"},
    "UnusedImports": {"desc": "Warn about unused imports"},
    "MultilineStrings": {"desc": "Warn about multiline strings"},
    "CompilerWarning": {"desc": "Warn about compiler issues"},
    "AttachedPropertyReuse": {
        "desc": "Warn if attached types from parent components aren't reused. This is handled by the QtQuick lint plugin. Use Quick.AttachedPropertyReuse instead."
    },
    "LintPluginWarnings": {"desc": "Warn if a qmllint plugin finds an issue"},
    "VarUsedBeforeDeclaration": {"desc": "Warn if a variable is used before declaration"},
    "InvalidLintDirective": {"desc": "Warn if an invalid qmllint comment is found"},
    "UseProperFunction": {"desc": "Warn if var is used for storing functions"},
    "AccessSingletonViaObject": {"desc": "Warn if a singleton is accessed via an object"},
    "TopLevelComponent": {"desc": "Fail when a top level Component are encountered"},
    "UncreatableType": {"desc": "Warn if uncreatable types are created"},
}


@unique
class WarningType(str, Enum):
    """Value that can be set in the ``type`` field of the qmllint JSON."""

    WARNING = "warning"
    INFO = "info"
    DISABLE = "disable"


class WarningDetails(TypedDict, total=True):
    """Details of a rule that has not been respected.

    The location of the violation of the rule is also given.

    The typical format is as follow:

    ```json
    {
        "column": <a column number>,
        "length": <the length of the sequence concerned by the warning>,
        "line": <a line number>,
        "message": "<details about the warning>",
        "type": "warning"
    }
    ```

    .. note:: Two other fields can be present, but are not represented here:
        - ``charOffset``: The precise position in the file of the start of the sequence affected by the warning
        - ``suggestions``: A list of suggestion to correct the warning (optional)
    """

    column: int
    """The column number at the start of the offending code sequence."""

    length: int
    """The lenght of the offending code sequence."""

    line: int
    """The line number at the start of the offending code sequence."""

    message: str
    """The message indicating which rule is not respected."""

    type: WarningType
    """The type of warning.``
    """


class FileDiagnostic(TypedDict, total=True):
    """A qmllint file diagnostic report.

    The typical format of an element is as follows:

    ```json
    {
        filename: <path to the file>
        success: <boolean indicating warning is empty>
        warning: [
            <a warning in the file>
        ]
    }
    ```

    ..seealso:: WarningDetails to have further details about the content in the list of the ``warning`` field.
    """

    filename: str
    """Path to the file."""

    success: bool
    """A boolean indicating if a least one rule has not been respected in the file.

    False if at least one rule has not been respected, True otherwise.

    If True, then ``warnings`` is an empty list.
    """

    warnings: list[WarningDetails]
    """A list of warning representing a rule that has not been respected.

    .. seealso:: WarningDetails
    """


class Report(TypedDict, total=True):
    """A qmllint report.

    The typical format of an element is as follows:

    ```json
    {
        files: [
            <a file diagnostic>,
        ]
    }
    ```

    ..seealso:: FileDiagnostic to have further details about the content in the list of the ``files`` field.
    """

    files: list[FileDiagnostic]
    """The list of the file analyzed.

    .. seealso:: FileDiagnostic
    """
