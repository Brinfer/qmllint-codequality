import QtQuick

Item {
    id: someId
    property alias myself: someId.myself // not ok: referring to itself

    property alias cycle: someId.cycle2 // not ok: indirectly referring to itself
    property alias cycle2: someId.cycle

    property alias indirect: someId.cycle // not ok: referring to alias indirectly referring to itself
}