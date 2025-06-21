# utils.py

import cv2
import base64
from io import BytesIO
from PIL import Image

def image_to_base64(image_array):
    _, buffer = cv2.imencode('.jpg', image_array)
    return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
