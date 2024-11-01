// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-multiline-strings.html

import QtQuick

Item {
    property string multiLine: "first
second
third"

    property string multiLine2: 'first
second
third'
}