import streamlit as st
from PIL import Image
from image_processing import process_image
import io

def upload_image():
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        return Image.open(uploaded_file)

def main():
    st.set_page_config(layout="wide")
    st.title("Real Time Document Processing with Translation")

    st.sidebar.title("Menu")
    img = upload_image()
    process_btn = st.sidebar.button("Process Image")

    if img is not None:
        st.sidebar.image(img, caption='Uploaded Image', use_column_width=True)

    if process_btn and img is not None:
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

if __name__ == "__main__":
    main()
