// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-incompatible-type.html
import QtQuick

Item {
    component MyType: QtObject {
        default property list<Item> myDefaultProperty
    }

    MyType {
        QtObject {} // note: QtObject does not inherit from Item
    }
}