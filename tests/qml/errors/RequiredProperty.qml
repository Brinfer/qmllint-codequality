# https://doc.qt.io/qt-6/qmllint-warnings-and-errors-required.html

import QtQuick

Item {
    component RepeatMe: Item {
        required property int index;
        required property int helloWorld;
    }

    RepeatMe {} // not ok: required properties index and helloWorld not set

    Repeater {
        model: 10
        RepeatMe {} // not ok: required property index set by Repeater, but not helloWorld
    }
}