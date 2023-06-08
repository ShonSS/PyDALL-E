from dotenv import load_dotenv
import openai
import os
from gallery import ImageGallery
from PyQt6.QtCore import QThread, pyqtSignal

class ImageGenerator(QThread):
    finished = pyqtSignal(list)

    def __init__(self, prompt, num_images, size):
        super().__init__()
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.urls = []

    def run(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = openai.Image.create(
                prompt=self.prompt,
                n=self.num_images,
                size=self.size,
                response_format="url"
            )
            self.urls = [data["url"] for data in response["data"]]
        except Exception as e:
            print(f"An error occurred: {e}")

        # Emit the finished signal with the generated image URLs
        self.finished.emit(self.urls)
