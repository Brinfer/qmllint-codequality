import QtQuick 2.15

Rectangle {
    width: 200
    height: 200

    readonly property int readOnlyValue: 42

    MouseArea {
        anchors.fill: parent
        onClicked: {
            parent.readOnlyValue = 100  // This will cause a ReadOnlyProperty error
        }
    }
}
