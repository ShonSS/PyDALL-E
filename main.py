# main.py
from PyQt6.QtWidgets import QApplication
from gui import ImageGeneratorApp
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = TimedRotatingFileHandler('log.txt', when='midnight', backupCount=7)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Exclude DEBUG level for the 'openai' logger
    openai_logger = logging.getLogger('openai')
    openai_logger.setLevel(logging.INFO)  # Change the logging level to INFO or higher

setup_logging()

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
