// This is an example of how to mark a property as deprecated in QML
Item {
    // @Deprecated: Use 'newProperty' instead of 'oldProperty'
    @Deprecated { reason: "Use newProperty instead" }
    property int oldProperty: 42

    property int newProperty: oldProperty

    Component.onCompleted: {
        console.log(oldProperty); // Warning: Property "oldProperty" is deprecated (Reason: Use newProperty instead)
    }
}
