import QtQuick

Rectangle {
    width: 200; height: 100
    color: "lightblue"

    Text {
        id: exampleText
        text: "Hello, World!"
        anchors.centerIn: parent
    }

    // Intentional AttachedPropertyReuse error
    Rectangle.AttachedProperty { }
}
