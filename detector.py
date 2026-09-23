#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 17:54:34 2022

@author: armin
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.neighbors import NearestNeighbors
PROJECT_DIR = Path(__file__).resolve().parent

# ---------------------------
# Load data
# ---------------------------
image_process_dir_1 : str | Path | None = PROJECT_DIR / "Image_process" / 'result.xlsx'
image_process_dir_2 : str | Path | None = PROJECT_DIR / "Image_process" / 'IMG_10.xlsx'



df1 = pd.read_excel(image_process_dir_1 , index_col=0)
df2 = pd.read_excel(image_process_dir_2 , index_col=0)

# Extract feature vectors
X1 = df1[['X', 'Y', 'val']].to_numpy()
X2 = df2[['X', 'Y', 'val']].to_numpy()

# ---------------------------
# Build nearest-neighbor models
# ---------------------------
nn1 = NearestNeighbors(n_neighbors=1).fit(X1)
nn2 = NearestNeighbors(n_neighbors=1).fit(X2)

# df1 -> df2 nearest neighbor
dist12, idx12 = nn2.kneighbors(X1)

# df2 -> df1 nearest neighbor
dist21, idx21 = nn1.kneighbors(X2)

# ---------------------------
# Mutual nearest neighbor matching
# ---------------------------
matched_df1 = []
matched_df2 = []

used_df2 = set()

for i in range(len(X1)):
    j = idx12[i][0]  # best match in df2

    # mutual check
    if idx21[j][0] == i and j not in used_df2:
        matched_df1.append(i)
        matched_df2.append(j)
        used_df2.add(j)

# ---------------------------
# Build results
# ---------------------------
df1_matched = df1.iloc[matched_df1].reset_index(drop=True)
df2_matched = df2.iloc[matched_df2].reset_index(drop=True)

df2_matched.columns = [c + "_match" for c in df2_matched.columns]


result = pd.concat([df1_matched, df2_matched], axis=1)

# ---------------------------
# Save
# ---------------------------
result_dir : str | Path | None = PROJECT_DIR / 'Image_process'
Path(result_dir).mkdir(parents=True, exist_ok=True)
result_path = result_dir / "result.xlsx"


result.to_excel(result_path, index=True)
