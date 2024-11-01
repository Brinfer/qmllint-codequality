import QtQuick

Item {
    id: root
    width: 200
    height: 200

    property int deferredWidth: child.width // Potential trigger for DeferredPropertyId error

    Loader {
        id: childLoader
        sourceComponent: child
        onLoaded: {
            // Accessing 'child.width' when 'child' may not be fully initialized
            console.log("Child width:", child.width)
        }
    }

    Component {
        id: child
        Rectangle {
            width: root.width / 2
            height: root.height / 2
            color: "blue"
        }
    }
}
