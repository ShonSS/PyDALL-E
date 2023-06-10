from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QFormLayout, \
    QStatusBar, QMainWindow, QDialog, QSizePolicy
from PyQt6.QtGui import QPalette, QColor, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt
from image_generator import ImageGenerator
from gallery import ImageGallery
from data import AESTHETICS
from boost_art_prompt_thread import BoostArtPromptThread
from themes import set_dark_mode, set_light_mode

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
        self.placeholderText = 'Describe your imagination... Boost it, select parameters, then create your art...'
        self.promptInput.setPlaceholderText(self.placeholderText)
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

        # Initialize the BoostArtPromptThread
        self.boostArtPromptThread = None

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
        if self.boostArtPromptThread and self.boostArtPromptThread.isRunning():
            return

        # Instantiate BoostArtPromptThread and begin execution
        self.boostArtPromptThread = BoostArtPromptThread(self.promptInput.toPlainText())
        self.boostArtPromptThread.promptBoosted.connect(self.update_prompt_input)
        self.boostArtPromptThread.finished.connect(self.handle_boost_prompt_finished)
        self.boostArtPromptThread.start()

        # Update the status bar while boosting the art prompt
        self.statusBar.showMessage("Boosting art prompt...")

    # Add this new event handler at the end of ImageGeneratorApp class
    def handle_boost_prompt_finished(self):
        # Reset the status bar message when the processing is finished
        self.statusBar.clearMessage()

    def update_prompt_input(self, boosted_prompt):
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

        # Show completion message
        self.statusBar.showMessage("Image generation completed.", 5000)  # Display for 5 seconds

    def handle_boost_prompt_finished(self):
        # Reset the status bar message when the processing is finished
        self.statusBar.showMessage("Art prompt boosting completed.", 5000)  # Display for 5 seconds

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