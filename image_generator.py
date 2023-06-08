# image_generator.py
from dotenv import load_dotenv
import openai
import os
from gallery import ImageGallery

class ImageGenerator:
    def __init__(self, prompt, num_images, size):
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.gallery = ImageGallery()

    def generate_images(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = openai.Image.create(
                prompt=self.prompt,
                n=self.num_images,
                size=self.size,
                response_format="url"
            )
            urls = [data["url"] for data in response["data"]]
            self.gallery.display_images(urls)
            self.gallery.show()  # Display the gallery
        except Exception as e:
            print(f"An error occurred: {e}")
