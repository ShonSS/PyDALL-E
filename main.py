from kivy.app import App
from gui_components import MainLayout
from api_handler import set_api_key
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class ImageGeneratorApp(App):
    def build(self):
        main_layout = MainLayout()
        return main_layout

if __name__ == "__main__":
    set_api_key(api_key)
    ImageGeneratorApp().run()