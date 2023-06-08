from dotenv import load_dotenv
import openai
import os
from gallery import ImageGallery

class ImageGenerator:
    def __init__(self, prompt, num_images, size, status_bar):
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.status_bar = status_bar
        self.urls = []  # Store the generated image URLs

    def generate_images(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            self.status_bar.showMessage(f"Generating {self.num_images} image(s) of size {self.size}...")
            response = openai.Image.create(
                prompt=self.prompt,
                n=self.num_images,
                size=self.size,
                response_format="url"
            )
            self.urls = [data["url"] for data in response["data"]]  # Store the generated image URLs
            self.status_bar.showMessage("Successfully generated images.")
            self.gallery.display_images(self.urls)
            self.gallery.show()
        except Exception as e:
            self.status_bar.showMessage(f"An error occurred: {e}")
