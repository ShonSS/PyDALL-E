from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout, QStatusBar, \
    QMainWindow
from PyQt6.QtCore import Qt
from image_generator import ImageGenerator
from gallery import ImageGallery


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

        # Create an instance of ImageGallery
        self.gallery = ImageGallery()
        self.gallery.hide()  # Hide the gallery initially

    def on_generate_click(self):
        self.gallery.clear_images()  # Clear previous images from the gallery

        # Create an instance of ImageGenerator and move it to a separate thread
        self.image_generator = ImageGenerator(self.promptInput.text(), int(self.numberInput.currentText()),
                                              self.sizeInput.currentText())
        self.image_generator.finished.connect(self.handle_image_generation_finished)
        self.image_generator.start()

        # Show a loading message or progress indicator while generating images
        self.statusBar.showMessage("Generating images...")

    def handle_image_generation_finished(self, urls):
        # Display the generated images in the gallery
        self.gallery.display_images(urls)
        self.gallery.show()

        # Reset the loading message or progress indicator
        self.statusBar.clearMessage()
