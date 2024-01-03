import easyocr
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from translation import translate_text


def process_image(img):
    reader = easyocr.Reader(['de'])
    img_np = np.array(img)
    result = reader.readtext(img_np)

    img_with_white_rectangles = img.copy()
    draw = ImageDraw.Draw(img_with_white_rectangles)

    aspect_ratio = img.size[0] / img_np.shape[1]

    for (bbox, _, _) in result:
        scaled_bbox = [
            (coord[0] * aspect_ratio, coord[1] * aspect_ratio)
            for coord in bbox
        ]

        top_left = tuple(scaled_bbox[0])
        bottom_right = tuple(scaled_bbox[2])

        # Adjust rectangle size to cover the original text
        draw.rectangle([top_left, bottom_right], fill="white")

    # Overlay translated text on the white rectangles
    draw_text_on_image(img_with_white_rectangles, result, aspect_ratio)

    return img_with_white_rectangles


def draw_text_on_image(img, result, aspect_ratio):
    draw = ImageDraw.Draw(img)
    default_font_size = 12
    small_font = ImageFont.truetype("arial.ttf", default_font_size)

    for (bbox, text, _) in result:
        scaled_bbox = [
            (coord[0] * aspect_ratio, coord[1] * aspect_ratio)
            for coord in bbox
        ]

        top_left = tuple(scaled_bbox[0])
        translated_text = translate_text(text)

        text_width, text_height = draw.textsize(translated_text, font=small_font)

        # Adjust text position relative to original text position
        text_position = (
            top_left[0] + ((scaled_bbox[2][0] - scaled_bbox[0][0]) - text_width) // 2,
            top_left[1] + ((scaled_bbox[2][1] - scaled_bbox[0][1]) - text_height) // 2
        )

        draw.text(text_position, translated_text, fill="black", font=small_font)

    return img
