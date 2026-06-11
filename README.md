# LoRa Link Quality Prediction using Remote Sensing and Machine Learning

## Overview

This project presents an automated framework for predicting LoRa signal quality using Sentinel-2 satellite imagery, machine learning, and wireless propagation modeling.

Traditional LoRa network planning relies on expensive field surveys and manual measurements. This system automates coverage estimation by extracting environmental information from satellite imagery and integrating it with propagation models to estimate signal strength in urban and suburban environments.

The framework combines:

* Sentinel-2 Remote Sensing Data
* QGIS-based Geospatial Processing
* Support Vector Machine (SVM) Classification
* Land Cover Mapping
* Okumura-Hata Propagation Modeling
* LoRa Estimated Signal Power (ESP) Prediction

---

## Problem Statement

Although LoRa can theoretically achieve communication ranges up to 15 km, real-world coverage is highly dependent on surrounding obstacles such as buildings, vegetation, and terrain.

Manual site surveys are costly and time-consuming. This project aims to automate LoRa coverage estimation by identifying environmental features directly from satellite imagery and incorporating them into wireless propagation analysis.

---

## Methodology

### Step 1: Satellite Data Acquisition

* Sentinel-2 Level-2A imagery collected from the Copernicus Open Access Hub.
* Cloud coverage kept below 10% for improved data quality.

### Step 2: Preprocessing in QGIS

* Spectral bands combined through layer stacking.
* False Color Composite (FCC) generated using NIR, Red, and Green bands.
* Training samples manually labeled for:

  * Buildings
  * Roads
  * Vegetation
  * Water
  * Soil

### Step 3: SVM Land Cover Classification

Features Used:

* Blue Band
* Green Band
* Red Band
* Near Infrared (NIR)
* NDVI
* NDWI

Model:

* Support Vector Machine (RBF Kernel)
* StandardScaler Normalization
* Train-Test Split: 70%-30%

### Step 4: Land Cover Map Generation

The trained SVM model classifies each pixel into:

| Class | Category   |
| ----- | ---------- |
| 0     | Buildings  |
| 1     | Roads      |
| 2     | Vegetation |
| 3     | Water      |
| 4     | Soil       |

Output:

* GeoTIFF Land Cover Map
* Visualized using QGIS

### Step 5: LoRa Signal Prediction

The system traces the communication path between:

* Gateway
* End Device

Obstacle-aware path analysis is performed.

Environment Detection:

* Building/Vegetation detected → Urban (NLOS)
* Clear path → Suburban (LOS)

The corresponding Okumura-Hata model is then applied to estimate signal strength.

---

## Project Architecture

Sentinel-2 Satellite Data

↓

QGIS Preprocessing

↓

Feature Extraction (NDVI, NDWI)

↓

SVM Classification

↓

Land Cover Map Generation

↓

Obstacle Detection

↓

Okumura-Hata Path Loss Model

↓

Estimated Signal Power (ESP)

---

## Results

### Scenario A – City Center

* Environment: Urban (NLOS)
* Obstacle Detected: Building
* Distance: 0.475 km
* Predicted Signal Strength: -99.34 dBm

### Scenario B – Open Road

* Environment: Suburban (LOS)
* Obstacle Detected: None
* Distance: 0.307 km
* Predicted Signal Strength: -82.8 dBm

The results demonstrate significant attenuation caused by urban obstacles and validate the effectiveness of the proposed hybrid AI-Physics framework.

---

## Technologies Used

### Programming

* Python

### Machine Learning

* Scikit-Learn
* Support Vector Machine (SVM)

### Geospatial Processing

* QGIS
* Rasterio

### Data Processing

* NumPy
* Pandas

### Visualization

* Matplotlib

### Remote Sensing

* Sentinel-2 Satellite Imagery

---

## Repository Structure

```text
LoRa-Implement/
│
├── classify_full_image.py
├── train_svm.py
├── esp_prediction.py
├── entire_map_view.py
├── README.md
├── scaler.pkl
├── svm_model.pkl
│
├── image/
│
├── lora/
│
└── landcover_map.tif
```

## Future Improvements

* 3D City Modeling using DSM Data
* Real-time LoRa Coverage Visualization
* Streamlit Web Dashboard
* Multi-Gateway Optimization
* Deep Learning-based Land Cover Classification

---

## Conclusion

This project demonstrates a practical integration of Remote Sensing, Machine Learning, and Wireless Communication Theory for automated LoRa network planning. By combining satellite imagery with SVM-based land cover classification and Okumura-Hata propagation modeling, the system provides realistic site-specific signal predictions without requiring extensive field surveys.

**#Developed by Harsh Tomar
M.Tech CSE, IIT Mandi
<img width="953" height="565" alt="image" src="https://github.com/user-attachments/assets/7ea48415-01ea-45bf-ac68-1e62a817bee9" />

