import QtQuick

Item {
    component Cycle: Cycle {} // not ok: directly inherits from itself
    component C: C2 {}        // not ok: indirectly inherits from itself
    component C2: C{}
}