# main_window.py
import logging
from PyQt6.QtGui import QPalette, QGuiApplication, QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QComboBox, QFormLayout, \
    QStatusBar, QMainWindow, QSizePolicy, QProgressBar, QDial, QLCDNumber
from boost_art_prompt_thread import BoostArtPromptThread
from data import AESTHETICS
from gallery import ImageGallery
from image_generator import ImageGenerator
from themes import set_dark_mode, set_light_mode

# Add logging at the start of the file
logging.getLogger(__name__)

class ImageGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDALL-E")

        # Set dark mode or light mode based on the system setting
        if QGuiApplication.palette().color(QPalette.ColorRole.Window).value() > 128:
            set_light_mode(self)
        else:
            set_dark_mode(self)

        # UI Elements
        self.promptInput = QPlainTextEdit(self)
        self.placeholderText = 'Craft your art prompt... Imagine your artistic vision and let AI assist you in exploring rich styles and elements. Click "Boost Art Prompt" to unleash your creativity!'
        self.promptInput.setPlaceholderText(self.placeholderText)

        # QDial and QLCDNumber for number of images
        self.imageNumberDial = QDial()
        self.imageNumberDial.setNotchesVisible(True)
        self.imageNumberDial.setRange(1, 10)
        self.imageNumberDisplay = QLCDNumber()
        self.imageNumberDisplay.setDigitCount(2)
        self.imageNumberDisplay.display(1)  # Set default value to 1

        # QDial and QLCDNumber for image size
        self.imageSizeDial = QDial()
        self.imageSizeDial.setNotchesVisible(True)
        self.imageSizeDial.setRange(1, 3)
        self.imageSizeDisplay = QLCDNumber()
        self.imageSizeDisplay.setDigitCount(4)
        self.imageSizeDisplay.display("256x256")  # Set default value to 256

        self.generateButton = QPushButton("Generate Artwork", self)
        self.boostButton = QPushButton("Boost Art Prompt", self)
        self.aestheticsDropdown = QComboBox(self)
        self.aestheticsDropdown.addItem("")
        self.aestheticsDropdown.addItems(AESTHETICS)

        self.selected_aesthetic = None  # Initialize the selected_aesthetic attribute

        # Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(100)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.imageGeneratorThread = None

        # Initialize the BoostArtPromptThread
        self.boostArtPromptThread = None

        # Layout
        layout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        formLayout = QFormLayout()

        formLayout.addRow(self.aestheticsDropdown)
        formLayout.addRow(self.promptInput)
        formLayout.addRow(self.boostButton)

        # Add QDial and QLCDNumber for number of images
        numberLayout = QHBoxLayout()
        numberLayout.addWidget(self.imageNumberDial)
        numberLayout.addWidget(self.imageNumberDisplay)
        formLayout.addRow(numberLayout)

        # Add QDial and QLCDNumber for image size
        sizeLayout = QHBoxLayout()
        sizeLayout.addWidget(self.imageSizeDial)
        sizeLayout.addWidget(self.imageSizeDisplay)
        formLayout.addRow(sizeLayout)

        formLayout.addRow(self.generateButton)
        layout.addLayout(formLayout)

        # Add progress bar to the layout
        layout.addWidget(self.progressBar)

        # Create an instance of ImageGallery
        self.gallery = ImageGallery()
        layout.addWidget(self.gallery)

        # Connect QDials and LCD displays
        self.imageSizeDial.valueChanged.connect(self.update_image_size_display)
        self.imageNumberDial.valueChanged.connect(self.update_image_number_display)

        # Connect buttons to methods
        self.generateButton.clicked.connect(self.generate_images)
        self.boostButton.clicked.connect(self.boost_prompt)

    def generate_images(self):
        """ Generates images based on the current input parameters """
        art_prompt = self.promptInput.toPlainText()
        aesthetics = self.aestheticsDropdown.currentText()
        num_images = self.imageNumberDial.value()
        image_size = self.imageSizeDisplay.value()  # Get actual image size from imageSizeDisplay

        # If no aesthetics is selected, default to 'none'
        if not aesthetics:
            aesthetics = 'none'

        # Clear the UI and update the status bar
        self.gallery.clear_images()
        self.statusBar.showMessage("Generating Artwork...")

        # Create an instance of ImageGenerator and start the thread
        self.imageGeneratorThread = ImageGenerator(art_prompt, num_images, image_size, aesthetics)
        self.imageGeneratorThread.progressChanged.connect(self.progressBar.setValue)
        self.imageGeneratorThread.finished.connect(self.on_image_generation_finished)
        self.imageGeneratorThread.finished.connect(self.display_images)  # Connect finished signal to display_images
        self.imageGeneratorThread.start()

    def display_images(self):
        """ Create a new ImageGallery, add images to it and display it """
        self.gallery = ImageGallery()  # Create a new ImageGallery
        self.gallery.display_images(self.imageGeneratorThread.image_urls)  # Display the images
        self.gallery.show()  # Show the ImageGallery

    def boost_prompt(self):
        art_prompt = self.promptInput.toPlainText()
        self.boostArtPromptThread = BoostArtPromptThread(art_prompt, self.selected_aesthetic)
        self.boostArtPromptThread.promptBoosted.connect(self.set_prompt)
        self.boostArtPromptThread.progressChanged.connect(self.update_progress)
        self.boostArtPromptThread.start()

    def on_image_generation_finished(self, results):
        """ Called once the thread for generating images is complete """
        logging.info(f"Image generation complete: {results}")
        self.statusBar.showMessage("Artwork Generated!")

    def set_prompt(self, boosted_prompt):
        """ Update the art prompt with the boosted version """
        logging.info(f"Art prompt boosted: {boosted_prompt}")
        self.promptInput.setPlainText(boosted_prompt)

    def update_progress(self, progress):
        """ Update the progress bar """
        self.progressBar.setValue(progress)

    def update_image_size_display(self, value):
        """ Update the display for image size """
        image_size = 256 * 2 ** (value - 1)
        self.imageSizeDisplay.display(f"{image_size}x{image_size}")

    def update_image_number_display(self, value):
        """ Update the display for number of images """
        self.imageNumberDisplay.display(value)

