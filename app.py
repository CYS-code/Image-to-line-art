{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import cv2\
import numpy as np\
import streamlit as st\
from PIL import Image\
import io\
\
def convert_to_line_art(image, blur=5, canny_thresh1=50, canny_thresh2=150, line_thickness=1):\
    # Convert image to grayscale\
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\
    \
    # Apply Gaussian Blur to smooth details\
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)\
    \
    # Detect edges using Canny\
    edges = cv2.Canny(blurred, threshold1=canny_thresh1, threshold2=canny_thresh2)\
    \
    # Invert the image to get a black-and-white line art effect\
    inverted = cv2.bitwise_not(edges)\
    \
    # Adjust line thickness (Dilation)\
    kernel = np.ones((line_thickness, line_thickness), np.uint8)\
    thick_lines = cv2.dilate(inverted, kernel, iterations=1)\
    \
    return thick_lines\
\
def main():\
    st.title("\uc0\u55356 \u57256  Image to Colouring Page Converter")\
    st.write("Upload an image, and I'll turn it into a black-and-white colouring page!")\
    \
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])\
    \
    if uploaded_file is not None:\
        # Read the uploaded image\
        image = Image.open(uploaded_file)\
        image_np = np.array(image)\
        image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)\
        \
        # User settings for line art conversion\
        blur = st.slider("Blur Intensity", 1, 15, 5, step=2)\
        canny1 = st.slider("Edge Detection: Threshold 1", 10, 200, 50)\
        canny2 = st.slider("Edge Detection: Threshold 2", 50, 300, 150)\
        thickness = st.slider("Line Thickness", 1, 5, 1)\
        \
        # Process the image\
        line_art = convert_to_line_art(image_cv2, blur, canny1, canny2, thickness)\
        \
        # Display the processed image\
        st.image(line_art, caption="Line Art Output", use_column_width=True, channels="GRAY")\
        \
        # Convert processed image to download format\
        result = Image.fromarray(line_art)\
        buf = io.BytesIO()\
        result.save(buf, format="PNG")\
        byte_im = buf.getvalue()\
        \
        # Provide download button\
        st.download_button(\
            label="Download Line Art Image",\
            data=byte_im,\
            file_name="line_art.png",\
            mime="image/png"\
        )\
\
if __name__ == "__main__":\
    main()\
}