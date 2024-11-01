// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-missing-property.html

import QtQuick

Item {
    component MyType: QtObject { property Item myItem; }

    MyType {
        Item {}
    }
}