# main.py
import openai
from PyQt6.QtWidgets import QApplication
import logging
from main_window import ImageGeneratorApp
import os
from dotenv import load_dotenv
from PyQt6.QtGui import QGuiApplication, QColor, QPalette
from qt_material import apply_stylesheet

# Configure logging settings
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def main():
    logging.info("Starting PyDALL-E")

    # Load the API key from the .env file
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        # Set the API key for the OpenAI library
        openai.api_key = openai_api_key
        logging.info("OpenAI API key loaded")
    else:
        raise ValueError("OpenAI API key not found in the .env file.")

    # Create the application
    app = QApplication([])

    # Get the current window color from the system palette
    default_color = QGuiApplication.palette().color(QPalette.ColorRole.Window)

    # Select a theme based on the lightness of the default window color
    if default_color.lightness() > 128:
        apply_stylesheet(app, theme='dark_purple.xml')
    else:
        apply_stylesheet(app, theme='light_purple.xml')

    logging.info("Application created")

    # Create and show the main window
    window = ImageGeneratorApp()
    window.show()
    logging.info("Main window shown")

    # Run the event loop
    logging.info("Entering event loop")
    app.exec()
    logging.info("Exiting PyDALL-E")


if __name__ == "__main__":
    main()