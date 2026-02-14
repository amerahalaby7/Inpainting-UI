from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
import io
import json
from functions import sam2model
import numpy as np
app = FastAPI()


@app.post("/inpaint/")
async def process_image(
    image: UploadFile = File(...),
    cordinates: str = Form(...)
):
    img_read = await image.read()
    print(f"Received image: {image.filename}, size: {len(img_read)} bytes")
    img = Image.open(io.BytesIO(img_read)).convert("RGB")
    coord = json.loads(cordinates)
    output = io.BytesIO()
    draw_image = sam2model(np.array(img), coord)
    draw_image = Image.fromarray(draw_image)
    # Here we will write anything to the image, for example, we can draw rectangles on the image based on the coordinates received from the form data.
    # draw = ImageDraw.Draw(img)
    # for c in coord:
    #     x1, y1, x2, y2 = c
    #     draw.rectangle([x1, y1, x2, y2], fill="black")
    draw_image.save(output, format="PNG")
    output.seek(0)
    return StreamingResponse(output, media_type="image/png")
