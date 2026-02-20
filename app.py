import streamlit as st
import requests
from PIL import Image
from PIL import UnidentifiedImageError
from io import BytesIO
from streamlit_image_coordinates import streamlit_image_coordinates

BASE_URL = "http://127.0.0.1:8000"

st.title("Image CRUD App")

# ---------------- UPLOAD ----------------
st.header("Upload Image")

image_id = st.number_input("Image ID", min_value=1, step=1)
uploaded_file = st.file_uploader("Choose image", type=["png", "jpg", "jpeg"])

if st.button("Upload"):
    if uploaded_file is not None:
        response = requests.post(
            f"{BASE_URL}/upload/{image_id}",
            files={"file": (uploaded_file.name, uploaded_file.getvalue())}
        )
        if response.ok:
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            st.success(payload['message'] if 'message' in payload else "Image uploaded successfully::")
        else:
            try:
                payload = response.json()
                error_message = payload.get("detail") or payload.get("message") or str(payload)
            except ValueError:
                error_message = response.text or "Unknown error"
            st.error(f"Upload failed ({response.status_code}): {error_message}")
    else:
        st.warning("Please choose an image first.")

# ---------------- SHOW IMAGES ----------------
st.header("Gallery")

response = requests.get(f"{BASE_URL}/images")
# print(response.status_code, response.text)
print(response.text)
images = response.json()
print("--"*100)
# print(images)
# print(images.items())
input_image_id = st.number_input("Enter Image ID to view", min_value=1, step=1)
show_images = st.button("Show Images")
if show_images:
    for img_id, data in images.items():
        if int(img_id) != input_image_id:
            continue
        image_response = requests.get(f"{BASE_URL}/image/{img_id}")
        print(image_response)
        print(image_response.status_code,"-----"*100, image_response.headers)
        if image_response.status_code != 200:
            st.error(f"Could not load image {img_id}: {image_response.status_code}")
            continue

        content_type = image_response.headers.get("content-type", "")
        print(f"Content-Type for image {img_id}: {content_type}")
        if not content_type.startswith("image/"):
            st.error(f"Invalid response for image {img_id}: {content_type or 'unknown content type'}")
            continue

        try:
            # print("--"*100, image_response.content)
            image = Image.open(BytesIO(image_response.content))
        except UnidentifiedImageError:
            st.error(f"Could not decode image {img_id}.")
            continue

        # Apply border color if toggled
        if data["colored"]:
            st.markdown(
                f"""
                <div style="border:5px solid red; padding:5px;">
                    <p>Image ID: {img_id}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write(f"Image ID: {img_id}")

        clicked = streamlit_image_coordinates(image, key=f"coords_{img_id}")
        if clicked:
            st.write(f"Clicked on image {img_id}: x={clicked['x']}, y={clicked['y']}")
