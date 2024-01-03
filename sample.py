import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import easyocr
from googletrans import Translator
import io
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

translator = Translator()
reader = easyocr.Reader(['de'])


def upload_image():
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        return Image.open(uploaded_file)


def process_image(img):
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

        draw.rectangle([top_left, bottom_right], fill="white")

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

        text_position = (
            top_left[0] + ((scaled_bbox[2][0] - scaled_bbox[0][0]) - text_width) // 2,
            top_left[1] + ((scaled_bbox[2][1] - scaled_bbox[0][1]) - text_height) // 2
        )

        draw.text(text_position, translated_text, fill="black", font=small_font)

    return img


def translate_text(text, target_language='en'):
    translation = translator.translate(text, dest=target_language)
    return translation.text


def main():
    st.set_page_config(layout="wide")
    st.title("Real Time Document Processing with Translation")

    st.sidebar.title("Menu")

    # Images Section
    st.sidebar.subheader("Images")
    img = upload_image()
    process_img_btn = st.sidebar.button("Process Image")

    if img is not None:
        st.sidebar.image(img, caption='Uploaded Image', use_column_width=True)

    if process_img_btn and img is not None:
        st.sidebar.text("Image is being processed...")
        processed_img = process_image(img)
        st.subheader("Processed Image with Translated Text")
        st.image(processed_img, caption='Translated Text on Processed Image', use_column_width=True)

        # Download button
        buffered = io.BytesIO()
        processed_img.save(buffered, format="PNG")
        buffered.seek(0)
        st.download_button(
            label="Download Processed Image",
            data=buffered,
            file_name="processed_image.png",
            mime="image/png",
        )

    # PDFs Section
    st.sidebar.subheader("PDFs")
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")

    if uploaded_pdf is not None:
        images = convert_from_path(uploaded_pdf.name)
        for image in images:
            st.image(image, caption='Original PDF Image')
            processed_image = process_image(image)
            st.image(processed_image, caption='Processed Image with Translated Text')


if __name__ == "__main__":
    main()
