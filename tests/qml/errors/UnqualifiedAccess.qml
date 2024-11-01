import QtQuick

Item {
    property int helloWorld
    Item {
        property int unqualifiedAccess: helloWorld + 1 // not ok: Unqualified access here.
    }
}
