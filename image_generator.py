# image_generator.py

from dotenv import load_dotenv
import openai
import os
from gallery import ImageGallery
from logger import setup_logger

class ImageGenerator:
    def __init__(self, prompt, num_images, size, status_bar):
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.status_bar = status_bar
        self.gallery = ImageGallery()
        self.logger = setup_logger(__name__)

    def generate_images(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            self.logger.debug(f"Generating {self.num_images} image(s) of size {self.size} for prompt '{self.prompt}'")
            self.status_bar.showMessage(f"Generating {self.num_images} image(s) of size {self.size}...")
            response = openai.Image.create(
                prompt=self.prompt,
                n=self.num_images,
                size=self.size,
                response_format="url"
            )
            urls = [data["url"] for data in response["data"]]
            self.logger.debug(f"Successfully generated images.")
            self.status_bar.showMessage("Successfully generated images.")
            self.gallery.display_images(urls)
            self.gallery.show()
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            self.status_bar.showMessage(f"An error occurred: {e}")
