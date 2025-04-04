import json
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

# Function to run shell commands
def execute_shell_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

# Function to parse the JSON file and process tasks
def process_tasks(file_path):
    # Read and print the raw content of the file
    with open(file_path, 'r') as file:
        raw_content = file.read()
        print("Raw content of the file:", raw_content)  # Print the raw content of the file
        
        # Now try loading the JSON data
        tasks = json.loads(raw_content)
    
    for task in tasks:
        # Extract task details
        task_id = task.get('id')
        start_time_str = task.get('start')
        end_time_str = task.get('end')
        tags = ' '.join(task.get('tags', []))
        
        # Execute the "start" command
        start_command = f"timew start '{tags}' {start_time_str}"
        execute_shell_command(start_command)

        # Execute the "stop" command if an end time is available
        if end_time_str:
            stop_command = f"timew stop {end_time_str}"
            execute_shell_command(stop_command)

# Main PyQt5 Application Window
class FileSelectorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select File to Process")
        self.setGeometry(100, 100, 300, 150)

        # Layout and widgets
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Choose a file to process", self)
        self.layout.addWidget(self.label)
        
        self.choose_file_button = QPushButton("Choose File", self)
        self.choose_file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.choose_file_button)

        self.process_button = QPushButton("Process Tasks", self)
        self.process_button.clicked.connect(self.process_file)
        self.process_button.setEnabled(False)  # Disable until a file is selected
        self.layout.addWidget(self.process_button)

        self.selected_file = None

        self.setLayout(self.layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            self.selected_file = file_path
            self.label.setText(f"Selected file: {file_path}")
            self.process_button.setEnabled(True)  # Enable the Process button after selecting a file

    def process_file(self):
        if self.selected_file:
            process_tasks(self.selected_file)  # Process the selected file

# Initialize the PyQt application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = FileSelectorWindow()
    window.show()

    sys.exit(app.exec_())
