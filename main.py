from PyQt6.QtWidgets import QApplication
from gui import ImageGeneratorApp


def main():
    # Create the application
    app = QApplication([])

    # Create and show the main window
    window = ImageGeneratorApp()
    window.show()

    # Run the event loop
    app.exec()


if __name__ == "__main__":
    main()
