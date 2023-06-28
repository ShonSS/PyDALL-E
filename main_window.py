# main_window.py
import logging

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QPalette, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, \
    QComboBox, QFormLayout, \
    QStatusBar, QMainWindow, QProgressBar, QDial, QLCDNumber

from boost_art_prompt_thread import BoostArtPromptThread
from data import AESTHETICS
from gallery import ImageGallery
from image_generator import ImageGenerator
from themes import set_dark_mode, set_light_mode

# Logging configuration
logger = logging.getLogger(__name__)


class ImageGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDALL-E")

        if QGuiApplication.palette().color(QPalette.ColorRole.Window).value() > 128:
            set_light_mode(self)
        else:
            set_dark_mode(self)

        self.promptInput = QPlainTextEdit(self)
        self.promptInput.setPlaceholderText('Craft your art prompt...')

        self.imageNumberDial = QDial()
        self.imageNumberDial.setNotchesVisible(True)
        self.imageNumberDial.setRange(1, 10)
        self.imageNumberDisplay = QLCDNumber()
        self.imageNumberDisplay.setDigitCount(2)
        self.imageNumberDisplay.display(1)

        self.imageSizeDial = QDial()
        self.imageSizeDial.setNotchesVisible(True)
        self.imageSizeDial.setRange(1, 3)
        self.imageSizeDisplay = QLCDNumber()
        self.imageSizeDisplay.setDigitCount(4)
        self.imageSizeDisplay.display("256x256")

        self.generateButton = QPushButton("Generate Artwork", self)
        self.boostButton = QPushButton("Boost Art Prompt", self)
        self.aestheticsDropdown = QComboBox(self)
        self.aestheticsDropdown.addItem("")
        self.aestheticsDropdown.addItems(AESTHETICS)

        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(100)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        layout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        formLayout = QFormLayout()
        formLayout.addRow(self.aestheticsDropdown)
        formLayout.addRow(self.promptInput)
        formLayout.addRow(self.boostButton)

        numberLayout = QHBoxLayout()
        numberLayout.addWidget(self.imageNumberDial)
        numberLayout.addWidget(self.imageNumberDisplay)
        formLayout.addRow(numberLayout)

        sizeLayout = QHBoxLayout()
        sizeLayout.addWidget(self.imageSizeDial)
        sizeLayout.addWidget(self.imageSizeDisplay)
        formLayout.addRow(sizeLayout)

        formLayout.addRow(self.generateButton)
        layout.addLayout(formLayout)

        layout.addWidget(self.progressBar)

        self.gallery = ImageGallery()

        self.imageSizeDial.valueChanged.connect(self.update_image_size_display)
        self.imageNumberDial.valueChanged.connect(self.update_image_number_display)

        self.generateButton.clicked.connect(self.generate_images)
        self.boostButton.clicked.connect(self.boost_prompt)

    def generate_images(self):
        art_prompt = self.promptInput.toPlainText()
        aesthetics = self.aestheticsDropdown.currentText()
        num_images = self.imageNumberDial.value()
        image_size_value = self.imageSizeDial.value()
        image_size = 256 * 2 ** (image_size_value - 1)
        image_size = f"{image_size}x{image_size}"

        if not aesthetics:
            aesthetics = 'none'

        self.statusBar.showMessage("Generating Artwork...")

        self.imageGeneratorThread = ImageGenerator(art_prompt, num_images, image_size, aesthetics)
        self.imageGeneratorThread.progressChanged.connect(self.progressBar.setValue)
        self.imageGeneratorThread.finished.connect(self.on_image_generation_finished)
        self.imageGeneratorThread.imageGenerated.connect(self.add_image_to_gallery)
        self.imageGeneratorThread.thumbnailGenerated.connect(self.add_thumbnail_to_gallery)

        self.imageGeneratorThread.start()

    def boost_prompt(self):
        art_prompt = self.promptInput.toPlainText()
        self.selected_aesthetic = self.aestheticsDropdown.currentText() or 'none'  # get selected aesthetic or default to 'none'
        self.boostArtPromptThread = BoostArtPromptThread(art_prompt, self.selected_aesthetic)
        self.boostArtPromptThread.promptBoosted.connect(self.set_prompt)
        self.boostArtPromptThread.progressChanged.connect(self.update_progress)
        self.boostArtPromptThread.start()

    def on_image_generation_finished(self):
        logger.info("Image generation complete")
        self.statusBar.showMessage("Artwork Generated!")
        self.gallery = ImageGallery()
        self.gallery.show()

    @pyqtSlot(QPixmap, str)
    def add_image_to_gallery(self, pixmap, url):
        """Add the generated image to the gallery."""
        self.gallery.add_image(pixmap, url)

    @pyqtSlot(QPixmap)
    def add_thumbnail_to_gallery(self, pixmap):
        """Add the generated thumbnail to the gallery."""
        self.gallery.add_thumbnail(pixmap)

    def set_prompt(self, boosted_prompt):
        logger.info(f"Art prompt boosted: {boosted_prompt}")
        self.promptInput.setPlainText(boosted_prompt)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def update_image_size_display(self, value):
        image_size = 256 * 2 ** (value - 1)
        self.imageSizeDisplay.display(f"{image_size}x{image_size}")

    def update_image_number_display(self, value):
        self.imageNumberDisplay.display(value)
