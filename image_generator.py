# image_generator.py
import logging
import openai
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)

class ImageGenerator(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal(list)
    thumbnailGenerated = pyqtSignal(bytes)  # Added thumbnailGenerated signal

    def __init__(self, prompt, num_images, size, selected_aesthetic=None):
        super().__init__()
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.urls = []
        self.selected_aesthetic = selected_aesthetic

    def run(self):
        logger.info("Starting image generation")

        # Generate images one by one to report progress
        for i in range(self.num_images):
            try:
                logger.info("Generating image %d", i + 1)
                response = openai.Image.create(
                    prompt=self.prompt,
                    n=1,
                    size=self.size,
                    response_format="url"
                )

                url = response["data"][0]["url"]
                self.urls.append(url)
                logger.info("Generated URL for image %d: %s", i + 1, url)

                # Generate thumbnail
                thumbnail_response = openai.Image.create(
                    prompt=self.prompt,
                    n=1,
                    size=self.size,
                    response_format="image"
                )
                thumbnail_bytes = thumbnail_response["data"][0]["image"]
                self.thumbnailGenerated.emit(thumbnail_bytes)  # Emit the thumbnailGenerated signal

            except Exception as e:
                logger.error("An error occurred during image generation: %s", str(e))

            # Emit progress update
            progress = int((i + 1) / self.num_images * 100)
            self.progressChanged.emit(progress)
            logger.debug("Image generation progress: %d%%", progress)

        # Emit the finished signal with the generated image URLs
        logger.info("Image generation completed")
        self.finished.emit(self.urls)

    def quit(self):
        super().quit()
        self.progressChanged.emit(0)
