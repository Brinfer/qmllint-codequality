// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-non-list-property.html
import QtQuick

Item {
    component MyComponent: QtObject {
        default property Item helloWorld
    }
    MyComponent {
        // first item bound to default property:
        Item { objectName: "first" } // will warn: Cannot assign multiple objects to a default non-list property [non-list-property]
        // second item bound to default property:
        Item { objectName: "second" } // not ok: default property was bound already
        // third item bound to default property:
        Item { objectName: "third" } // not ok: default property was bound already

        Component.onCompleted: console.log(helloWorld.objectName) // prints "third"
    }
}