// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-access-singleton-via-object.html

import QtQml
import QtQuick as QQ

QtObject {
    id: root
    // Cannot access singleton as a property of an object. Did you want to access an attached object?
    property var singletonAccess: root.QQ.Application.platform
}