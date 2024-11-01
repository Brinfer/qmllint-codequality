import QtQuick
import QtQuick.Controls // Unused import, will cause UnusedImport error

Rectangle {
    width: 200
    height: 200
    color: "lightblue"

    Text {
        id: helloText
        text: "Hello, World!"
        anchors.centerIn: parent
    }
}
