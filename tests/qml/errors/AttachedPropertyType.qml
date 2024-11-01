// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-attached-property-reuse.html
import QtQuick

Item {
    QtObject {
        LayoutMirroring.enabled: true
    }
}