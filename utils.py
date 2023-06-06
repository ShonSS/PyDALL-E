import logging
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from io import BytesIO
import requests
from tempfile import NamedTemporaryFile
from kivy.uix.image import Image

def configure_logging():
    logging.basicConfig(filename='pydall_e_app.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

def get_kivy_image_from_url(url):
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(requests.get(url).content)
    temp_file.close()

    img = Image(source=temp_file.name, allow_stretch=True, keep_ratio=True, size_hint=(.5, .5))
    return img