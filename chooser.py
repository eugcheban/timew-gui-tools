import os
import sys
import subprocess
from PySide6.QtCore import QObject, Slot, QAbstractListModel, QModelIndex, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Signal


class TagModel(QAbstractListModel):
    TagRole = Qt.UserRole + 1

    def __init__(self, tags=None):
        super().__init__()
        self._tags = tags or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._tags)

    def data(self, index, role):
        if not index.isValid() or role != self.TagRole:
            return None
        return self._tags[index.row()]

    def roleNames(self):
        return {self.TagRole: b'tag'}

    def setTags(self, tags):
        self.beginResetModel()
        self._tags = tags
        self.endResetModel()

class GetFuncionality(QObject):
    def __init__(self, tag_model):
        super().__init__()
        self._tag_model = tag_model
    
    @Slot(str)
    def executeTag(self, tag_name):
        result = subprocess.run(['timew', 'start ', tag_name], capture_output=True, text=True)
        print(f'Executing {tag_name}: {result}')
        

class TagFetcher(QObject):
    tagsUpdated = Signal(list)  # Signal to notify QML when tags are updated

    def __init__(self, tag_model):
        super().__init__()
        self._tag_model = tag_model

    @Slot()
    def fetchTags(self):
        try:
            print("Fetching tags...")
            result = subprocess.run(['timew', 'tags'], capture_output=True, text=True)
            print("Command output:", result.stdout)

            lines = result.stdout.split("\n")
            tags = []

            for line in lines:
                if line.strip() and not line.startswith("Tag") and not line.startswith("-"):
                    tag = line.split("  ")[0].strip()
                    tags.append(tag)

            print("Parsed tags:", tags)
            self._tag_model.setTags(tags)  # Update the model with fetched tags
            self.tagsUpdated.emit(tags)  # Emit signal with updated tags
        except Exception as e:
            print(f"Error fetching tags: {e}")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Stop all other tracks
    subprocess.run(['timew', 'stop'], text=True)
    # Create engine and load QML file
    engine = QQmlApplicationEngine()

    # Create TagModel and TagFetcher instances
    tag_model = TagModel()
    tag_fetcher = TagFetcher(tag_model)
    functionality = GetFuncionality(tag_model)

    # Expose objects to QML
    engine.rootContext().setContextProperty("tagModel", tag_model)
    engine.rootContext().setContextProperty("tagFetcher", tag_fetcher)
    engine.rootContext().setContextProperty("getFunctionality", functionality)

    # Determine the absolute path to Main.qml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "Example", "Main.qml")

    # Load Main.qml
    engine.load(qml_file_path)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
