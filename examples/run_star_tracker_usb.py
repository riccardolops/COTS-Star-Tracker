#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time
import os
import numpy as np

####################################
# USER CONFIG
####################################

CAMERA_INDEX = 2  # /dev/video0
OUTPUT_DIR = "star_images"
NUM_IMAGES = 30  # number of frames to capture
CAPTURE_INTERVAL = 1.0  # seconds between images

IMAGE_PREFIX = "star"
IMAGE_EXT = ".jpg"

####################################
# CREATE OUTPUT DIRECTORY
####################################

os.makedirs(OUTPUT_DIR, exist_ok=True)

####################################
# OPEN USB CAMERA
####################################

print("[INFO] Opening USB camera...")
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)

if not cap.isOpened():
    raise RuntimeError("Cannot open USB camera")

# -------- Camera tuning (CRITICAL for stars) --------
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # manual exposure
cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # adjust for your camera
cap.set(cv2.CAP_PROP_GAIN, 0)
cap.set(cv2.CAP_PROP_FPS, 5)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# ---------------------------------------------------

print("[INFO] Letting camera stabilize...")
time.sleep(2)

####################################
# IMAGE ACQUISITION LOOP
####################################

print(f"[INFO] Capturing {NUM_IMAGES} images...")

for i in range(NUM_IMAGES):
    ret, frame = cap.read()
    if not ret:
        print(f"[WARNING] Failed to capture frame {i}")
        continue

    # Convert to grayscale (recommended for star tracker)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    filename = os.path.join(OUTPUT_DIR, f"{IMAGE_PREFIX}_{i:04d}{IMAGE_EXT}")

    cv2.imwrite(filename, gray)
    print(f"[INFO] Saved {filename}")

    time.sleep(CAPTURE_INTERVAL)

####################################
# CLEANUP
####################################

cap.release()
print("[INFO] Capture complete.")
