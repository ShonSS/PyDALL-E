import os
import openai
import logging

def set_api_key(api_key):
    openai.api_key = api_key

def send_request(prompt, num_images, size):
    try:
        response = openai.Image.create(
          prompt=prompt,
          n=num_images,
          size=size,
          model="image-alpha-001",
          response_format="url",
        )
        return response
    except Exception as e:
        logging.exception("Failed to send a request to the API")
        raise e

def validate_input(prompt, num_images, size):
    is_valid_prompt = len(prompt) > 0
    is_valid_num_images = 1 <= num_images <= 10
    is_valid_size = size in ["128x128", "256x256", "512x512", "1024x1024"]

    return is_valid_prompt and is_valid_num_images and is_valid_size