# gallery.py
import requests
from functools import partial
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QVBoxLayout, QWidget, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import time


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class ImageGallery(QMainWindow):
    imageClicked = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setWindowTitle('Generated Artwork')

        # Set the background color specifically for the central_widget:
        self.central_widget.setStyleSheet("background-color: black;")

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.image_labels = []  # Store the labels for the images

        # Set the maximum size of the gallery window
        self.setMaximumWidth(800)
        self.setMaximumHeight(600)

        # Add the status bar
        self.statusBar().showMessage("Ready")

    def display_images(self, urls):
        start_time = time.time()
        resolutions = set()
        total_size_bytes = 0

        # Clear previous images
        self.clear_images()

        for i, url in enumerate(urls):
            # Download the image
            response = requests.get(url)
            image_data = response.content
            total_size_bytes += len(image_data)

            # Convert the image data to QPixmap and add it to a ClickableLabel as a thumbnail
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            resolutions.add(f"{pixmap.width()}x{pixmap.height()}")
            thumbnail = pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)

            label = ClickableLabel()
            label.setPixmap(thumbnail)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.setObjectName(f"thumbnail_{i}")
            label.clicked.connect(partial(self.display_full_size_image, pixmap))

            # Add the ClickableLabel to the layout
            row = i // 3  # 3 images per row
            col = i % 3
            self.grid_layout.addWidget(label, row, col)

            # Store the label for later use
            self.image_labels.append(label)

        elapsed_time = time.time() - start_time

        self.statusBar().showMessage(f"Generated {len(urls)} image(s) in {elapsed_time:.2f} seconds. Sizes: {', '.join(resolutions)}. Total size: {total_size_bytes / 1024:.1f} KB")

    def clear_images(self):
        # Remove and delete the image labels
        for label in self.image_labels:
            label.deleteLater()

        # Clear the list of image labels
        self.image_labels = []

    def display_full_size_image(self, pixmap):
        dialog = QDialog(self)
        dialog.setWindowTitle("Full-sized Image")
        dialog.setFixedSize(QSize(pixmap.width(), pixmap.height()))

        label = QLabel(dialog)
        label.setPixmap(pixmap)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        dialog.setLayout(vbox)
        dialog.exec()