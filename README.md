# QMLLint Code-Quality

## Overview

`qmllint-codequality` is a Python tool designed to convert the JSON output of the `qmllint` command line into a standardized code-quality format JSON. This makes it easier to integrate QML linting results into various code quality tools and CI/CD pipelines.

## What is qmllint?

`qmllint` is a tool provided by Qt that verifies the syntactic validity of QML files and warns about common QML anti-patterns. It helps developers ensure their QML code is both correct and follows best practices.
`qmllint` can be configured to disable specific warnings or change how they are treated, making it a flexible tool for maintaining high code quality.

## Features

- **JSON Conversion**: Converts `qmllint` JSON output to a standardized code quality format.
- **Easy Integration**: Facilitates integration with code quality tools and CI/CD pipelines.

## Usage

To use QMLLint Code Quality Converter, run the following command:

```bash
qmllint-codequality path/to/qmllint/output.json
```

### Command Line Options

If you want to explore more options that can be passed on the command-line, you can use the `--help` option:

```bash
qmllint-codequality --help
```

And you should see something like:

```bash
usage: qmllint-codequality [-h] [-V] [-v {WARNING,INFO,DEBUG}] input_file output_file

CLI app for converting qmllint JSON report to Code Quality JSON report.

positional arguments:
  input_file            The path to the qmllint JSON output to be converted
  output_file           output filename to write JSON to (default: clang-tidy.json)

options:
  -h, --help            show this help message and exit
  -V, --version         print the qmllint-codequality version and exit
  -v {WARNING,INFO,DEBUG}, --verbosity {WARNING,INFO,DEBUG}
                        indicates the level of verbosity
```
