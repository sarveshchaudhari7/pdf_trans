from pdf2image import convert_from_bytes
from image_processing import process_image

def convert_pdf_to_images(pdf_data):
    images = convert_from_bytes(pdf_data)
    return images

def process_pdf(pdf_data):
    pdf_images = convert_pdf_to_images(pdf_data)

    processed_images = []
    for img in pdf_images:
        processed_img = process_image(img)
        processed_images.append(processed_img)

    return processed_images
