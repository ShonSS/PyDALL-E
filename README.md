# PyDALL-E

PyDALL-E is a Python-based Kivy GUI application that allows users to generate images from textual descriptions using OpenAI's DALL-E API.

## Features

- User-friendly interface
- Customizable image generation settings (number of images and size)
- Asynchronous API requests ensure a responsive UI
- Display generated images on the screen
- Informative error messages

## Installation & Setup

1. Clone the repository: `git clone https://github.com/yourusername/PyDALL-E.git cd PyDALL-E`

2. Create a virtual environment and activate it: `python3 -m venv venv source venv/bin/activate # On Windows, use venv\Scripts\activate
`
3. Install the required dependencies: `pip install -r requirements.txt
`
4. Set your [OpenAI API Key](https://beta.openai.com/signup/):

`export OPENAI_API_KEY=your_api_key_here # On Windows, use set
`
## Usage

1. Run the application: `python main.py`

2. Enter a description in the text box.

3. Configure the number of images (1-10) and the image size (128x128, 256x256, 512x512, 1024x1024).

4. Click the "Create Art" button to generate and display the images based on the given description.

5. The progress bar at the bottom updates as the images are being loaded.

## Known Issues

- Some combinations of configurations may result in crashes due to Kivy's threading limitations, though the provided solution should work correctly for most cases.

## Contributing

Feel free to contribute by submitting pull requests or reporting issues to improve the project.

## License

This project is licensed under the MIT License.