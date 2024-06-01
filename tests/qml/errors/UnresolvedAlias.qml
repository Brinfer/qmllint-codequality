import QtQuick

Item {
    id: someId
    property int helloWorld

    property alias helloWorldAlias: helloWorld      // not ok: aliases have to refer by id
    property alias helloWorldAlias2: someId.helloWorlddd    // not ok: no helloWorlddd in someId
    property alias helloWorldAlias3: someIddd.helloWorld    // not ok: someIddd does not exist
}