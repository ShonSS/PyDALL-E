import requests
from functools import partial
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class ImageGallery(QWidget):
    imageClicked = pyqtSignal(QPixmap)

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

            # Convert the image data to QPixmap and add it to a ClickableLabel as a thumbnail
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            thumbnail = pixmap.scaledToWidth(150)

            label = ClickableLabel()
            label.setPixmap(thumbnail)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.setObjectName(f"thumbnail_{i}")
            label.clicked.connect(partial(self.handle_image_clicked, label))

            # Add the ClickableLabel to the layout
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

    def handle_image_clicked(self, label):
        pixmap = label.pixmap()
        self.imageClicked.emit(pixmap)