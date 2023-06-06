from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from api_handler import send_request, validate_input
from utils import configure_logging, get_kivy_image_from_url


configure_logging()


def create_dropdown(values, hint_text):
    dropdown = DropDown(auto_dismiss=True)
    for value in values:
        btn = Button(text=value, size_hint_y=None, height=30)
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn)

    main_button = Button(text=hint_text, on_release=dropdown.open)
    dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
    return main_button, dropdown


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(orientation="vertical", **kwargs)

        self.text_input = TextInput(hint_text="Enter your description here", multiline=True, size_hint_y=None,
                                    height=300)
        self.add_widget(self.text_input)

        config_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)

        self.num_images_button, num_images_dropdown = create_dropdown([str(i) for i in range(1, 11)],
                                                                      "Number of Images")
        config_layout.add_widget(self.num_images_button)

        self.size_button, size_dropdown = create_dropdown(["128x128", "256x256", "512x512", "1024x1024"], "Image Size")
        config_layout.add_widget(self.size_button)

        self.add_widget(config_layout)

        generate_button = Button(text="Create Art", size_hint_y=None, height=40)
        generate_button.bind(on_press=self.generate_image)
        self.add_widget(generate_button)

        self.image_display = GridLayout(cols=2, spacing=10, padding=[10, 10, 10, 10])
        self.add_widget(self.image_display)

        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=10)
        self.add_widget(self.progress_bar)

    def generate_image(self, instance):
        user_input = self.text_input.text
        num_images = int(self.num_images_button.text)
        image_size = self.size_button.text

        if validate_input(user_input, num_images, image_size):
            try:
                api_response = send_request(user_input, num_images, image_size)
                img_urls = [image_info["url"] for image_info in api_response.data]

                if len(img_urls) > 0:
                    for i, img_url in enumerate(img_urls):
                        self.progress_bar.value = (i + 1) * 100 / num_images
                        kivy_image = get_kivy_image_from_url(img_url)
                        self.image_display.add_widget(kivy_image)

                else:
                    error_message = f"Error: No images returned"
                    self.show_error_message(error_message)

            except Exception as e:
                self.show_error_message(str(e))

            finally:
                self.progress_bar.value = 0

    def show_error_message(self, message):
        error_label = Label(text=message, color=(1, 0, 0, 1), size_hint_y=None, height=20)
        self.add_widget(error_label)