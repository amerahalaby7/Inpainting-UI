import numpy as np
import cv2
from ultralytics import SAM
from typing import List

def sam2model(src_img: np.ndarray, coordinates: List[int]):
    model = SAM("sam2.1_b.pt")
    insam=model(src_img,points=coordinates)#,save=True)
    insam=insam[0]
    mask=insam.masks.data[0].cpu().numpy().astype(np.uint8)
    no_backgrnd= cv2.bitwise_and(src_img, src_img, mask=mask)
    return no_backgrnd