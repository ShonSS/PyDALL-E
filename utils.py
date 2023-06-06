import logging
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from io import BytesIO
import requests

def configure_logging():
    logging.basicConfig(filename='pydall_e_app.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

def get_kivy_image_from_url(url):
    core_image = CoreImage(BytesIO(requests.get(url).content), ext="png")
    kivy_image = KivyImage(texture=core_image.texture)
    return kivy_image