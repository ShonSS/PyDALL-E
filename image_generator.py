# image_generator.py
import logging

import openai
import requests
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

logger = logging.getLogger(__name__)


class ImageGenerator(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal(list)
    thumbnailGenerated = pyqtSignal(QPixmap)  # Emit QPixmap instead
    imageGenerated = pyqtSignal(QPixmap, str)  # Emit QPixmap and URL of each image

    def __init__(self, prompt, num_images, size, selected_aesthetic=None):
        super().__init__()
        self.prompt = prompt
        self.num_images = num_images
        self.size = size
        self.urls = []
        self.selected_aesthetic = selected_aesthetic

    def run(self):
        logger.info("Starting image generation")

        for i in range(self.num_images):
            try:
                logger.info("Generating image %d", i + 1)
                response = openai.Image.create(
                    prompt=self.prompt,
                    n=1,
                    size=self.size,
                    response_format="url"  # Get the image as url
                )

                image_url = response.data[0]["url"]

                # Download image from url
                image_data = requests.get(image_url).content

                # convert image data into QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)

                # generate a thumbnail by scaling down the original
                thumbnail = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio)

                self.thumbnailGenerated.emit(thumbnail)
                self.imageGenerated.emit(pixmap, image_url)  # Emit pixmap and URL of each image

                self.urls.append(image_url)
                logger.info("Generated URL for image %d: %s", i + 1, image_url)

            except Exception as e:
                logger.error("An error occurred during image generation: %s", str(e))

            progress = int((i + 1) / self.num_images * 100)
            self.progressChanged.emit(progress)
            logger.debug("Image generation progress: %d%%", progress)

        logger.info("Image generation completed")
        self.finished.emit(self.urls)

    def quit(self):
        super().quit()
        self.progressChanged.emit(0)
