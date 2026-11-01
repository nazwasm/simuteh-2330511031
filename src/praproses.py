"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""
import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,
    "gamma": 1.0,
    "clahe_clip": 2.0,
    "clahe_tile": 8,
    "penapis": "median",
    "kernel": 5,
    "sigma": 1.0,
    "tajam_k": 0.0,
}

def praproses(img_bgr, p=None):
    """Urutan: ubah ukuran -> gamma -> CLAHE kanal V -> redam derau -> tajamkan."""
    p = {**PARAM_BAWAAN, **(p or {})}
    
    # 1: Ubah ukuran agar lebar = p["lebar"], rasio aspek tetap
    h, w = img_bgr.shape[:2]
    rasio = p["lebar"] / w
    img = cv2.resize(img_bgr, (p["lebar"], int(h * rasio)), interpolation=cv2.INTER_AREA)
    
    # 2: Koreksi Gamma
    if p["gamma"] != 1.0:
        lut = np.array([255 * (i / 255) ** p["gamma"] for i in range(256)]).clip(0, 255).astype(np.uint8)
        img = cv2.LUT(img, lut)
        
    # 3: CLAHE Kanal V
    if p["clahe_clip"] > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        clahe = cv2.createCLAHE(clipLimit=p["clahe_clip"], tileGridSize=(p["clahe_tile"], p["clahe_tile"]))
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    # 4: Redam derau
    if p["penapis"] == "median":
        img = cv2.medianBlur(img, p["kernel"])
    elif p["penapis"] == "gaussian":
        img = cv2.GaussianBlur(img, (p["kernel"], p["kernel"]), p["sigma"])
        
    # 5: Tajamkan (Unsharp Masking)
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1 + p["tajam_k"], blur, -p["tajam_k"], 0)
        
    return img

def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
