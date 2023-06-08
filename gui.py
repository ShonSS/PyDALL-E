# gui.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout, QStatusBar, \
    QMainWindow
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from gallery import ImageGallery
from image_generator import ImageGenerator


class ImageGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDALL-E")

        # UI Elements
        self.promptInput = QLineEdit(self)
        self.numberInput = QComboBox(self)
        self.numberInput.addItems([str(i) for i in range(1, 11)])  # for example 1-10 images
        self.sizeInput = QComboBox(self)
        self.sizeInput.addItems(["256x256", "512x512", "1024x1024"])
        self.generateButton = QPushButton("Generate Artwork", self)
        self.generateButton.clicked.connect(self.on_generate_click)

        self.gallery = ImageGallery()

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Layout
        self.layout = QFormLayout()
        self.layout.addRow("Art Prompt:", self.promptInput)
        self.layout.addRow("Number of Images:", self.numberInput)
        self.layout.addRow("Image Size:", self.sizeInput)
        self.layout.addRow(self.generateButton)

        # Central Widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def on_generate_click(self):
        self.gallery.clear_images()  # Clear previous images from the gallery

        self.image_generator = ImageGenerator(self.promptInput.text(), int(self.numberInput.currentText()),
                                              self.sizeInput.currentText(), self.statusBar)
        self.image_generator.gallery = self.gallery  # Pass the gallery instance to ImageGenerator
        self.image_generator.generate_images()

        # Display the generated images in the gallery
        self.gallery.display_images(self.image_generator.urls)
        self.gallery.show()
