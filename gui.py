from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QFormLayout, QStatusBar, QMainWindow, QDialog
from PyQt6.QtGui import QPalette, QColor, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy
from image_generator import ImageGenerator
from gallery import ImageGallery
from data import AESTHETICS

import openai

class ImageGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDALL-E")

        # Set dark mode or light mode based on the system setting
        if QGuiApplication.palette().color(QPalette.ColorRole.Window).value() > 128:
            self.set_light_mode()
        else:
            self.set_dark_mode()

        # UI Elements
        self.promptInput = QPlainTextEdit(self)
        self.numberInput = QComboBox(self)
        self.numberInput.addItems([str(i) for i in range(1, 11)])  # for example 1-10 images
        self.sizeInput = QComboBox(self)
        self.sizeInput.addItems(["256x256", "512x512", "1024x1024"])
        self.generateButton = QPushButton("Generate Artwork", self)
        self.boostButton = QPushButton("Boost Art Prompt", self)
        self.aestheticsDropdown = QComboBox(self)
        self.aestheticsDropdown.addItems(AESTHETICS)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.imageGeneratorThread = None

        # Layout
        layout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        formLayout = QFormLayout()

        formLayout.addRow("Art Prompt:", self.promptInput)
        formLayout.addRow(self.boostButton)
        formLayout.addRow("Aesthetics:", self.aestheticsDropdown)
        formLayout.addRow("Number of Images:", self.numberInput)
        formLayout.addRow("Image Size:", self.sizeInput)
        formLayout.addRow(self.generateButton)
        layout.addLayout(formLayout)

        # Create an instance of ImageGallery
        self.gallery = ImageGallery()
        self.gallery.hide()  # Hide the gallery initially

        # Set the central widget's layout properties
        centralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Connect the buttons to their event handlers
        self.boostButton.clicked.connect(self.on_boost_prompt_click)
        self.generateButton.clicked.connect(self.on_generate_click)

    def on_boost_prompt_click(self):
        prompt = self.promptInput.toPlainText()

        # Call OpenAI to boost the art prompt and update the prompt input
        boosted_prompt = self.boost_art_prompt(prompt)
        self.promptInput.setPlainText(boosted_prompt)

    def on_generate_click(self):
        if self.imageGeneratorThread and self.imageGeneratorThread.isRunning():
            return

        # Destroy the previous image gallery
        self.gallery.deleteLater()

        self.gallery = ImageGallery()  # Create a new instance of ImageGallery
        self.gallery.hide()  # Hide the gallery initially

        self.gallery.clear_images()  # Clear previous images from the gallery

        # Create an instance of ImageGenerator and move it to a separate thread
        self.imageGeneratorThread = ImageGenerator(self.promptInput.toPlainText(), int(self.numberInput.currentText()),
                                                   self.sizeInput.currentText())
        self.imageGeneratorThread.progressChanged.connect(self.handle_image_generation_progress)
        self.imageGeneratorThread.finished.connect(self.handle_image_generation_finished)
        self.imageGeneratorThread.start()

        # Show a loading message or progress indicator while generating images
        self.statusBar.showMessage("Generating images...")

    def handle_image_generation_progress(self, progress):
        self.statusBar.showMessage(f"Generating images... Progress: {progress}%")

    def handle_image_generation_finished(self, urls):
        # Display the generated images in the gallery
        self.gallery.display_images(urls)
        self.gallery.show()

        # Reset the loading message or progress indicator
        self.statusBar.clearMessage()

    def boost_art_prompt(self, prompt):
        # Define the boost instruction
        boost_instruction = "Craft an art prompt for DALL-E by transforming the following text into a powerful catalyst for awe-inspiring art:"

        # Combine the boost instruction with the existing prompt
        combined_prompt = f"{boost_instruction} {prompt}"

        # Use OpenAI to rewrite the art prompt and engineer the best prompt
        # You can customize this logic according to your requirements
        boosted_prompt = openai.Completion.create(
            engine="text-davinci-003",
            prompt=combined_prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        ).choices[0].text.strip()

        return boosted_prompt

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
        palette.setColor(QPalette.ColorRole.Text, QColor("white"))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
        self.setPalette(palette)

    def set_light_mode(self):
        # Reset to the default palette for light mode
        self.setPalette(QGuiApplication.palette())

    def show_full_image(self, pixmap):
        full_image_dialog = QDialog(self)
        full_image_dialog.setWindowTitle("Full Size Image")

        full_image_label = QLabel()
        full_image_label.setPixmap(pixmap)
        full_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(full_image_label)

        full_image_dialog.setLayout(layout)
        full_image_dialog.exec_()
