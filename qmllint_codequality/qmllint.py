"""Module providing a collection of class representing a qmllint report.

It's mostly TypedDict.
It facilitate dictionary/JSON manipulation, representing a report in qmllint format.
"""

import re
from enum import Enum, unique
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Any


class Rules(str, Enum):
    """Enumeration of know rules used by qmllint.

    A rule is composed of its name, and a regex patterns used to retrieve the value from a message produced by qmllint.

    The special rule UNKNOWN i used in the case where it was not possible tp retrieve the rule from the message.
    """

    def __new__(cls, value: str, *_: "Any") -> "Rules":
        """Create a new rule.

        :param value: The rule name, in PascalCase format.
        :type value: str
        :param _: A list of argument, ignored here
        :type _: Any
        :return: A new rule
        :rtype: Rules
        """
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __init__(self, _: str, patterns: tuple[re.Pattern] | None = None) -> None:
        """Initialize a new Rule object.

        :param _: The value of the rule (used in __new__, and ignored here)
        :type _: str
        :param patterns: A list of message pattern, None if unknown, defaults to None
        :type patterns: tuple[re.Pattern] | None, optional
        """
        self.patterns = patterns

    @staticmethod
    def from_message(message: str) -> "Rules":
        """Determine the rule from the diagnostic message.

        :param message: The diagnostic's message.
        :type message: str
        :return: The rule, UNKNOWN if not found.
        :rtype: str
        """
        for rule in Rules:
            if rule.patterns is not None:
                for pattern in rule.patterns:
                    if pattern.match(message):
                        return rule

        return Rules.UNKNOWN

    UNKNOWN = ("UnknownRule",)
    """Special type indicating that the rule is not known."""

    ANCHORS_USAGE = ("AnchorsUsage", (re.compile(r"Using anchors here"),))
    """Warn about anchors that are used not effectively for optimal layout management and performance."""

    IMPORT_FAILURE = (
        "ImportFailure",
        (
            re.compile(r"Warnings occurred while importing module \".*\":"),
            re.compile(r"Failed to import .*\. Are your import paths set up properly\?"),
            re.compile(r"Item was not found. Did you add all import paths?"),
        ),
    )
    """Warn about failing imports and deprecated qmltypes."""

    UNUSED_IMPORTS = ("UnusedImports", (re.compile(r"Unused import at .*"),))
    """"Warns about unused QML imports."""

    READ_ONLY_PROPERTY = (
        "ReadOnlyProperty",
        (re.compile(r"Cannot assign to read-only property .*"), re.compile(r".*Can't assign to read-only property .*")),
    )
    """Warn about writing to read-only properties."""

    DEFERRED_PROPERTY_ID = (
        "DeferredPropertyId",
        (re.compile(r"Could not compile binding for .*: Cannot load property .*"),),
    )
    """Warn about making deferred properties immediate by giving them an id."""

    DUPLICATED_NAME = ("DuplicatedName", (re.compile(r"Found a duplicated id. id .* was first declared at .*"),))
    """Warns if there are multiple declarations of the same name within the QML file."""

    PREFIXED_IMPORT_TYPE = ("PrefixedImportType",)
    """Warns if import types are prefixed inconsistently or incorrectly."""

    ACCESS_SINGLETON_VIA_OBJECT = (
        "AccessSingletonViaObject",
        (re.compile(r"Cannot load singleton as property of object"),),
    )
    """Warns about accessing QML singletons through object instances rather than directly."""

    DEPRECATED = (
        "Deprecated",
        (re.compile(r"Property \".*\" is deprecated.*"),),
    )
    """Warns about usage of deprecated QML features or APIs."""

    CONTROLS_SANITY = ("ControlsSanity",)
    """Warns about inconsistencies or potential issues in QML controls."""

    UNRESOLVED_TYPE = (
        "UnresolvedType",
        [
            re.compile(r".* is used but it is not resolved"),
            re.compile(r".* was not found. Did you add all import paths\?"),
        ],
    )
    """Warns if a referenced QML type cannot be resolved."""

    LINT_PLUGIN_WARNINGS = ("LintPluginWarnings",)
    """Warns about issues reported by lint plugins configured for qmllint."""

    MULTILINE_STRINGS = ("MultilineStrings",)
    """Warns about the usage of multiline strings, which may impact readability or maintainability."""

    RESTRICTED_TYPE = ("RestrictedType",)
    """Warns about usage of QML types that are restricted or not recommended."""

    PROPERTY_ALIAS_CYCLES = (
        "PropertyAliasCycles",
        (re.compile(r"Alias \".*\" is part of an alias cycle"),),
    )
    """Warns about cycles in property aliases, which may lead to unexpected behavior."""

    VAR_USED_BEFORE_DECLARATION = ("VarUsedBeforeDeclaration",)
    """Warns if 'var' is used before it's declared."""

    ATTACHED_PROPERTY_REUSE = ("AttachedPropertyReuse",)
    """Warns about reusing attached properties in an inconsistent or incorrect manner."""

    REQUIRED_PROPERTY = (
        "RequiredProperty",
        (re.compile(r"Component is missing required property .* from .*"),),
    )
    """Warns about missing required properties in QML components."""

    WITH_STATEMENT = (
        "WithStatement",
        (
            re.compile(
                r"with statements are strongly discouraged in QML and might cause false positives when analysing unqualified identifiers"
            ),
        ),
    )
    """Warns about usage of the 'with' statement in QML, which is generally discouraged."""

    INHERITANCE_CYCLE = ("InheritanceCycle", (re.compile(r" is part of an inheritance cycle: "),))
    """Warns about cycles in QML component inheritance."""

    UNCREATABLE_TYPE = (
        "UncreatableType",
        (re.compile(r"Object type is not derived from QObject or QQmlComponent\..*"),),
    )
    """Warns if a QML type cannot be instantiated."""

    MISSING_PROPERTY = ("MissingProperty", (re.compile(r"Property \".*\" not found on type \".*\""),))
    """Warns about missing properties that are expected to be present in QML components."""

    INVALID_LINT_DIRECTIVE = ("InvalidLintDirective",)
    """Warns about invalid lint directives used in QML code."""

    COMPILER_WARNINGS = (
        "CompilerWarnings",
        (re.compile(r"Could not compile binding for .*"),),
    )
    """Warns about potential issues or inconsistencies detected during QML compilation."""

    USE_PROPER_FUNCTION = ("UseProperFunction",)
    """Warns about incorrect usage of functions in QML."""

    NON_LIST_PROPERTY = (
        "NonListProperty",
        (re.compile(r"Cannot assign multiple objects to a default non-list property"),),
    )
    """Warns about incorrect usage of non-list properties in QML."""

    INCOMPATIBLE_TYPE = ("IncompatibleType",)
    """Warns about incompatible types used in QML bindings."""

    TOP_LEVEL_COMPONENT = ("TopLevelComponent",)
    """Warns about issues related to top-level components in QML files."""

    MISSING_TYPE = ("MissingType",)
    """Warns about missing QML types that are referenced but not defined."""

    DUPLICATE_PROPERTY_BINDING = (
        "DuplicatePropertyBinding",
        (
            re.compile(r"Duplicate interceptor on property \".*\""),
            re.compile(r"Duplicate value source on property \".*\""),
            re.compile(r"Cannot combine value source and binding on property \".*\""),
        ),
    )
    """Warns about duplicate property bindings in QML components."""

    BAD_SIGNAL_HANDLER_PARAMETERS = ("BadSignalHandlerParameters", (re.compile(r"Declared signal handler \".*\""),))
    """Warns about incorrect parameters in signal handlers."""

    UNQUALIFIED_ACCESS = (
        "UnqualifiedAccess",
        (re.compile(r"Unqualified access"),),
    )
    """Warns about unqualified access."""

    UNQUALIFIED_ALIAS = (
        "UnresolvedAlias",
        (re.compile(r"Cannot resolve alias \".*\""),),
    )
    """Warns about unqualified access."""

    ID_QUOTATION = ("IdQuotation", (re.compile(r"ids do not need quotation marks"),))


@unique
class WarningType(str, Enum):
    """Value that can be set in the ``type`` field of the qmllint JSON."""

    WARNING = "warning"
    INFO = "info"
    DISABLE = "disable"
    CRITICAL = "critical"


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
    """The length of the offending code sequence."""

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
