import numpy as np
import cv2
from ultralytics import SAM

def sam2model(src_img,coordinates):
    model = SAM("sam2.1_hiera_large.pt")
    insam=model(src_img,points=coordinates,save=True)
    insam=insam[0]
    mask=insam.masks.data[0].cpu().numpy().astype(np.uint8)
    no_backgrnd= cv2.bitwise_and(src_img, src_img, mask=mask)
    return no_backgrnd
    