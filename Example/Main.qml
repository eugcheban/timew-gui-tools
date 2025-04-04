import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    width: 300
    height: 400
    visible: true
    title: "timew chooser"

    // Dark theme colors
    color: "#121212"

    // List of tags (populated dynamically from Python backend)
    property var tags: []
    property var filteredTags: tags
    property string selectedTag: ""
    property int currentIndex: -1 // Tracks the currently highlighted index

    Component.onCompleted: {
        console.log("Connecting tagFetcher signal...");
        
        // Connect signal FIRST
        tagFetcher.tagsUpdated.connect(function(updatedTags) {
            console.log("Tags updated:", updatedTags);
            tags = updatedTags;
            filteredTags = updatedTags;
        });

        // THEN call fetchTags()
        tagFetcher.fetchTags();
        // Activate text field on start
        filterField.forceActiveFocus();
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        // TextField for filtering tags and executing on Enter
        TextField {
            id: filterField
            placeholderText: "Type to filter tags..."
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            color: "#FFFFFF"

            Keys.onPressed: (event) => {
                if (event.key === Qt.Key_Down && filteredTags.length > 0) {
                    currentIndex = Math.min(currentIndex + 1, filteredTags.length - 1);
                    selectedTag = filteredTags[currentIndex];
                    console.log("Navigated Down:", selectedTag);
                } else if (event.key === Qt.Key_Up && filteredTags.length > 0) {
                    currentIndex = Math.max(currentIndex - 1, 0);
                    selectedTag = filteredTags[currentIndex];
                    console.log("Navigated Up:", selectedTag);
                } else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                    if (selectedTag !== "") {
                        getFunctionality.executeTag(selectedTag);
                        Qt.quit();
                    } else {
                        getFunctionality.executeTag(filteredTags[0]);
                        Qt.quit();
                    }
                } else if(event.key == Qt.Key_Escape) {
                    Qt.quit();
                }
            }

            // Update filteredTags when text changes
            onTextChanged: {
                filteredTags = tags.filter(tag => tag.toLowerCase().includes(filterField.text.toLowerCase()));
                currentIndex = -1; // Reset index when filtering changes
                selectedTag = ""; // Reset selection when filtering changes
            }
        }

        // ListView for displaying and selecting tags
        ListView {
            id: tagListView
            Layout.fillWidth: true
            Layout.fillHeight: true

            model: filteredTags

            delegate: Item {
                width: tagListView.width
                height: 40

                Rectangle {
                    width: parent.width
                    height: parent.height
                    color: modelData === selectedTag ? "#87CEFA" : "#1E1E1E"
                    border.color: "#CCCCCC"
                    border.width: 1

                    Text {
                        text: modelData
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        verticalAlignment: Text.AlignVCenter
                        color: "#FFFFFF"
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            selectedTag = modelData;
                            currentIndex = index; // Update current index when clicked
                            console.log("Selected tag:", selectedTag);
                        }
                        onDoubleClicked: {
                            getFunctionality.executeTag(modelData)
                            Qt.quit();
                            // Add your double-click action here if needed
                        }
                    }
                }
            }
        }

    }
}
