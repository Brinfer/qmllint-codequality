import QtQuick

Rectangle {
    width: 200
    height: 200
    color: "lightblue"

    Text {
        id: errorText
        text: "This will cause an AnchorUsage error"
        anchors.right: errorText.left // Intentional mistake: An item cannot be anchored to itself
        anchors.verticalCenter: parent.verticalCenter
    }
}
