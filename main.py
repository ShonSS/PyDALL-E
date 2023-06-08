# main.py
from PyQt6.QtWidgets import QApplication
from gui import ImageGeneratorApp
import sys

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = ImageGeneratorApp()
    window.show()

    # Run the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
