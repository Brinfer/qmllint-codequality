import QtQuick
import QtQuick.Controls

Rectangle {
    id: rectangle
    width: 1920
    height: 1080

    readonly property color backgroundColor: "#c2c2c2"

    color: backgroundColor

    Button {
        id: button
        text: qsTr("Press me")
        anchors.verticalCenter: parent.verticalCenter
        checkable: true
        anchors.horizontalCenter: parent.horizontalCenter

        Connections {
            target: button
            function onClicked() {
                animation.start()
            }
        }
    }

    Text {
        id: label
        text: qsTr("Hello Test")
        anchors.top: button.bottom
        anchors.topMargin: 45
        anchors.horizontalCenter: parent.horizontalCenter

        SequentialAnimation {
            id: animation

            ColorAnimation {
                id: colorAnimation1
                target: rectangle
                property: "color"
                to: "#2294c6"
                from: backgroundColor
            }

            ColorAnimation {
                id: colorAnimation2
                target: rectangle
                property: "color"
                to: backgroundColor
                from: "#2294c6"
            }
        }
    }
    states: [
        State {
            name: "clicked"
            when: button.checked

            PropertyChanges {
                target: label
                text: qsTr("Button Checked")
            }
        }
    ]
}
