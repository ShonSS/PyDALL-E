from dotenv import load_dotenv
import openai
import os
from PyQt6.QtCore import QThread, pyqtSignal


class ImageGenerator(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self, prompt, num_images, size):
        super().__init__()
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.urls = []

    def run(self):
        # Load API key and initialize OpenAI
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Generate images one by one to report progress
        for i in range(self.num_images):
            try:
                response = openai.Image.create(
                    prompt=self.prompt,
                    n=1,
                    size=self.size,
                    response_format="url"
                )

                url = response["data"][0]["url"]
                self.urls.append(url)

            except Exception as e:
                print(f"An error occurred: {e}")

            # Emit progress update
            progress = int((i + 1) / self.num_images * 100)
            self.progressChanged.emit(progress)

        # Emit the finished signal with the generated image URLs
        self.finished.emit(self.urls)

    def quit(self):
        super().quit()
        self.progressChanged.emit(0)