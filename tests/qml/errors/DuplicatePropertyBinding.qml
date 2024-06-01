import QtQuick

Item {
    Rectangle {
        Behavior on width {
            NumberAnimation { duration: 1000 }
        }
        Behavior on width { // not ok: Duplicate interceptor on property "width" [duplicate-property-binding]
            NumberAnimation { duration: 2000 }
        }
    }

    Rectangle {
        NumberAnimation on x { to: 50; duration: 1000 }
        NumberAnimation on x { to: 10; duration: 100 } // not ok: Duplicate value source on property "x" [duplicate-property-binding]

        onXChanged: console.log(x)
    }

    Rectangle {
        NumberAnimation on x { to: 50; duration: 1000 } // not ok: Cannot combine value source and binding on property "x" [duplicate-property-binding]
        x: 55

        onXChanged: console.log(x)
    }

}