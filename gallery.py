# gallery.py
import requests
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap, QColor


class ImageGallery(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowTitle('Generated Artwork')

        self.setStyleSheet("background-color: black;")

        self.image_labels = []  # Store the labels for the images

        # Set the maximum size of the gallery window
        self.setMaximumWidth(800)
        self.setMaximumHeight(600)

    def display_images(self, urls):
        # Clear previous images
        self.clear_images()

        for i, url in enumerate(urls):
            # Download the image
            response = requests.get(url)
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

            # Store the label for later use
            self.image_labels.append(label)

    def clear_images(self):
        # Remove and delete the image labels
        for label in self.image_labels:
            label.deleteLater()

        # Clear the list of image labels
        self.image_labels = []
