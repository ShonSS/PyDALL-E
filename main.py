import openai
from PyQt6.QtWidgets import QApplication
from main_window import ImageGeneratorApp
import os
from dotenv import load_dotenv

def main():
    # Load the API key from the .env file
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        # Set the API key for the OpenAI library
        openai.api_key = openai_api_key
    else:
        raise ValueError("OpenAI API key not found in the .env file.")

    # Create the application
    app = QApplication([])

    # Create and show the main window
    window = ImageGeneratorApp()
    window.show()

    # Run the event loop
    app.exec()

if __name__ == "__main__":
    main()