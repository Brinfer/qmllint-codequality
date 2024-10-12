// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-attached-property-reuse.html
import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Material // contains the Material attached type

T.ToolBar {
    id: control

    // first instantiation of Material's attached property
    property color c: Material.toolBarColor

    background: Rectangle {
         // second instantiation of Material's attached property, wrong!
        color: Material.toolBarColor
    }
}