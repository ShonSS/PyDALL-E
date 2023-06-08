# gui.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from image_generator import ImageGenerator

class ImageGeneratorApp(QWidget):
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

        # Layout
        self.layout = QFormLayout()
        self.layout.addRow("Art Prompt:", self.promptInput)
        self.layout.addRow("Number of Images:", self.numberInput)
        self.layout.addRow("Image Size:", self.sizeInput)
        self.layout.addRow(self.generateButton)
        self.setLayout(self.layout)

    def on_generate_click(self):
        self.image_generator = ImageGenerator(self.promptInput.text(), int(self.numberInput.currentText()), self.sizeInput.currentText())
        self.image_generator.generate_images()
