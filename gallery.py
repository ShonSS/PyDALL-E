# gallery.py
import requests
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap


class ImageGallery(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def display_images(self, urls):
        for i in range(len(urls)):
            # Download the image
            response = requests.get(urls[i])
            image_data = response.content

            # Convert the image data to QPixmap and add it to a QLabel
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            label = QLabel()
            label.setPixmap(pixmap)

            # Add the QLabel to the layout
            row = i // 3  # 3 images per row
            col = i % 3
            self.layout.addWidget(label, row, col)
