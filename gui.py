from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QFormLayout, QStatusBar, QMainWindow, QDialog
from PyQt6.QtGui import QPalette, QColor, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy
from image_generator import ImageGenerator
from gallery import ImageGallery


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
        self.generateButton.clicked.connect(self.on_generate_click)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.imageGeneratorThread = None

        # Layout
        self.layout = QFormLayout()
        self.layout.addRow("Art Prompt:", self.promptInput)
        self.layout.addRow("Number of Images:", self.numberInput)
        self.layout.addRow("Image Size:", self.sizeInput)
        self.layout.addRow(self.generateButton)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # Central Widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        # Create an instance of ImageGallery
        self.gallery = ImageGallery()
        self.gallery.hide()  # Hide the gallery initially

        # Set the central widget's layout properties
        self.centralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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
        full_image_dialog.exec()