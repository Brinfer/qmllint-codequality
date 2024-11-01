// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-duplicate-property-binding.html
import QtQuick

Rectangle {
    Behavior on width {
        NumberAnimation { duration: 1000 }
    }
    Behavior on width { // not ok: Duplicate interceptor on property "width" [duplicate-property-binding]
        NumberAnimation { duration: 2000 }
    }
}