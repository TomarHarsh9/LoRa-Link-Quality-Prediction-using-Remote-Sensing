import numpy as np
import rasterio
from sklearn.svm import SVC
import joblib

#  Load trained SVM model

svm = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

#  Read required bands

def read_band(path):
    with rasterio.open(path) as src:
        return src.read(1).astype("float32")

B03 = read_band(r"C:\Users\Harsh\Downloads\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\GRANULE\L2A_T43RGM_A054757_20251216T053634\IMG_DATA\R10m\T43RGM_20251216T053251_B03_10m.jp2"
)   # Green
B02 = read_band(r"C:\Users\Harsh\Downloads\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\GRANULE\L2A_T43RGM_A054757_20251216T053634\IMG_DATA\R10m\T43RGM_20251216T053251_B02_10m.jp2"
)   # Blue
B04 = read_band(r"C:\Users\Harsh\Downloads\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\GRANULE\L2A_T43RGM_A054757_20251216T053634\IMG_DATA\R10m\T43RGM_20251216T053251_B04_10m.jp2"
)   # Red
B08 = read_band(r"C:\Users\Harsh\Downloads\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\GRANULE\L2A_T43RGM_A054757_20251216T053634\IMG_DATA\R10m\T43RGM_20251216T053251_B08_10m.jp2"
)   # NIR

#  Compute NDVI and NDWI

epsilon = 1e-10

NDVI = (B08 - B04) / (B08 + B04 + epsilon)
NDWI = (B03 - B08) / (B03 + B08 + epsilon)

#  Build feature matrix for all pixels

rows, cols = B02.shape
num_pixels = rows * cols

X_full = np.column_stack((
    B02.reshape(num_pixels),
    B03.reshape(num_pixels),
    B04.reshape(num_pixels),
    B08.reshape(num_pixels),
    NDVI.reshape(num_pixels),
    NDWI.reshape(num_pixels)
))
X_full = scaler.transform(X_full)

#  Predict land-cover class for each pixel
# 0 = building
# 1 = road
# 2 = vegetation
# 3 = water
# 4 = soil

y_pred = svm.predict(X_full)

#  Reshape prediction back to image

classified_map = y_pred.reshape(rows, cols)

#  Save classification map
 
B02_path = r"C:\Users\Harsh\Downloads\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\S2A_MSIL2A_20251216T053251_N0511_R105_T43RGM_20251216T085813.SAFE\GRANULE\L2A_T43RGM_A054757_20251216T053634\IMG_DATA\R10m\T43RGM_20251216T053251_B02_10m.jp2"

with rasterio.open(B02_path) as src:
    meta_crs = src.crs
    meta_transform = src.transform

with rasterio.open(
    "landcover_map.tif",
    "w",
    driver="GTiff",
    height=rows,
    width=cols,
    count=1,
    dtype=classified_map.dtype,
    crs=meta_crs,
    transform=meta_transform,

) as dst:
    dst.write(classified_map, 1)

print(" land-cover map generated")
