// https://doc.qt.io/qt-6/qmllint-warnings-and-errors-inheritance-cycle.html
import QtQuick

Item {
    component Cycle: Cycle {} // not ok: directly inherits from itself
    component C: C2 {}        // not ok: indirectly inherits from itself
    component C2: C{}
}