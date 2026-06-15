#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star detection script — rewritten for performance.
Original: May 23 2022
@author: armin
"""

import sys
import cv2
import numpy as np
import pandas as pd


# ── Load image ────────────────────────────────────────────────────────────────
IMAGE_PATH = '/Users/armin/Downloads/IMG_0444.jpg'

img = cv2.imread("IMG_0444.jpg")
if img is None:
    sys.exit(f"Error: could not load image at '{IMAGE_PATH}'\n"
             "Check that the file exists and the path is correct.")

gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
                       cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


# ── Build binary matrix (vectorised — replaces nested Python loops) ───────────
# Original: O(H*W) Python iterations; this is a single C-level NumPy op.
matrix = np.where(thresh == 255, 0, 1).astype(np.uint8)


# ── Find connected components (replaces recursive DFS Solution class) ─────────
# cv2.connectedComponentsWithStats is implemented in C and handles large images
# without hitting Python's recursion limit.
#
# stats columns:
#   CC_STAT_LEFT, CC_STAT_TOP, CC_STAT_WIDTH, CC_STAT_HEIGHT, CC_STAT_AREA
#
# Label 0 is the background — skip it.

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    matrix, connectivity=4   # 4-connectivity matches original up/down/left/right DFS
)

# Get one representative pixel per label in a single O(H*W) scan.
# np.unique returns the index of the first occurrence of each label.
_, first_idx = np.unique(labels.ravel(), return_index=True)
first_r, first_c = np.unravel_index(first_idx, labels.shape)

MIN_AREA = 3  # components smaller than this are treated as noise

star_map = [
    [int(first_r[label]), int(first_c[label]), int(stats[label, cv2.CC_STAT_AREA])]
    for label in range(1, num_labels)   # label 0 is background
    if stats[label, cv2.CC_STAT_AREA] >= MIN_AREA
]


# ── Build DataFrame (same columns as original) ────────────────────────────────
df = pd.DataFrame(star_map, columns=['X', 'Y', 'val'])

# ── Export to Excel (ExcelWriter.save() is deprecated since openpyxl 3.1) ────
with pd.ExcelWriter('0444.xlsx', engine='openpyxl') as datatoexcel:
    df.to_excel(datatoexcel)
