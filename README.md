# PyDALL-E

![img.png](img.png)

PyDALL-E is a groundbreaking Python-based GUI application that fuses the power of your imagination and OpenAI's state-of-the-art DALL-E API to transform textual descriptions into spellbinding visual art. The app harnesses PyQt6 to deliver an intuitive, user-centric interface, and embraces multithreading for a seamless, engaging, and responsive user experience.

Explore AI-powered art generation like never before with features such as AI prompt boosting for superior image generation, an aesthetic selector to refine your creations, and a gallery layout to display your masterpieces. Exciting enhancements on the horizon include upgraded art prompt design processes, performance tuning, UI/UX improvements, and AI completion refinements.

As you venture into the world of AI-driven creativity, PyDALL-E allows you to experiment with countless combinations of prompts and aesthetics, uncovering emergent properties and unlocking the limitless potential of your artistic pursuits.

## Features

- User-friendly interface with responsive design
- Generate images based on text descriptions
- AI prompt boosting for better image generation
- Aesthetic selector to refine generated art
- Customize the number of images and image size
- Asynchronous API requests for a smooth user experience
- Display generated images in a gallery layout
- Informative error handling
- Logging functionality for diagnostics

## Installation & Setup

An installer will be provided in a future update; until then:

1. Clone the repository: `git clone https://github.com/yourusername/PyDALL-E.git cd PyDALL-E`

2. Create a virtual environment and activate it:
   - On macOS and Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```

3. Install the required dependencies: `pip install -r requirements.txt`

4. Set your [OpenAI API Key](https://beta.openai.com/signup/):
   - On macOS and Linux:
     ```
     export OPENAI_API_KEY=your_api_key_here
     ```
   - On Windows (Command Prompt):
     ```
     set OPENAI_API_KEY=your_api_key_here
     ```
     or (PowerShell):
     ```
     $env:OPENAI_API_KEY="your_api_key_here"
     ```

## Usage

1. Run the application: `python main.py`
2. Enter a brief description in the text box that captures your imagination.
3. Use the "Boost Art Prompt" button to augment your idea, optionally selecting an aesthetic from the dropdown to refine the artistic style.
4. Configure the number of images (1-10) and the image size (256x256, 512x512, 1024x1024) to bring your vision to life.
5. Click the "Generate Artwork" button to create and display the images in a separate gallery, unveiling the AI-powered masterpieces.
6. The status and progress bars at the bottom keep you informed as your images are being generated.

## Known Issues

- GUI refinements and Image gallery are currently under development.
- Lack of an installer, planned for a future update.

## Future Features

- Upgraded art prompt design process to boost the quality of the generated art, such as more dropdowns to specify art parameters based on the DALL-E Prompt Book.
- GUI performance tuning
- GUI UI/UX enhancements
- AI Completion refinements

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to submit pull requests or report issues to help improve the project.

## Acknowledgements

- [OpenAI](https://openai.com) for their coding assistance and models
- [The DALL·E 2 Prompt Book](https://dallery.gallery/the-dalle-2-prompt-book/) for inspiration and art prompt ideas
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [PyCharm](https://www.jetbrains.com/pycharm/) for the IDE
- [Aesthetics Wiki](https://aesthetics.fandom.com/wiki/List_of_Aesthetics) for the list of aesthetics

## License

This project is licensed under the MIT License.
