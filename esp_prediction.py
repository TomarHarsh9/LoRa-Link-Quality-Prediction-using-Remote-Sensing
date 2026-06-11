import rasterio
import numpy as np
from skimage.draw import line

LANDCOVER_PATH = "landcover_map.tif"



P_TX = 14.0        # Transmit power (dBm)
F_MHZ = 868.0      # Frequency (MHz)
PIXEL_SIZE = 10.0  # meters (Sentinel-2)

print("Enter Deive location:")
row_tx = int(input("\nTX row: "))
col_tx = int(input("\nTX col: "))

print("\nEnter Gateway location:")
row_gw = int(input("\nGW row: "))
col_gw = int(input("\nGW col: "))

TX_HEIGHT = float(input("\nEnter device height (m): "))
GW_HEIGHT = float(input("Enter gateway height (m): "))

with rasterio.open(LANDCOVER_PATH) as src:
    landcover = src.read(1)

# Get pixel coordinates along TX–GW straight line
rr, cc = line(row_tx, col_tx, row_gw, col_gw)

# Extract land-cover classes along the path
path_classes = landcover[rr, cc]

# Extract land-cover classes 
INTERSECTION_CLASSES = {0, 2}  # 0=building, 2=vegetation
obstacles = [c for c in path_classes if c in INTERSECTION_CLASSES]

# ENVIRONMENT DECISION (URBAN / SUBURBAN)
def decide_environment(obstacles):
    # Building or vegetation present then  Urban (NLOS)
    if any(c in [0, 2] for c in obstacles):
        return "urban"
    else:
        return "suburban"

environment = decide_environment(obstacles)

#  DISTANCE COMPUTATION

def pixel_distance(row1, col1, row2, col2, pixel_size):
    d_m = np.sqrt((row1 - row2)**2 + (col1 - col2)**2) * pixel_size
    return d_m / 1000.0  # convert to km

distance_km = pixel_distance(
    row_tx, col_tx,
    row_gw, col_gw,
    PIXEL_SIZE
)

# OKUMURA–HATA MODELS 

# F_mhz = frequency in Mhz 
# d_Km = distance(btw h_gw or h_tx ) in km 
# h_gw = heigh of gateway (Meter)
# h_tx = height of transmiter(device) ( Meter)
# P_tx  = transmiter power
# L = path_loss  
def okumura_hata_urban(f_mhz, d_km, h_gw, h_tx):
    a_htx = (1.1 * np.log10(f_mhz) - 0.7) * h_tx - (1.56 * np.log10(f_mhz) - 0.8)
    L = (
        69.55
        + 26.16 * np.log10(f_mhz)
        - 13.82 * np.log10(h_gw)
        - a_htx
        + (44.9 - 6.55 * np.log10(h_gw)) * np.log10(d_km)
    )
    return L


def okumura_hata_suburban(L_urban, f_mhz):
    return L_urban - 2 * (np.log10(f_mhz / 28))**2 - 5.4


# ESP COMPUTATION (FINAL OUTPUT)

def compute_esp(P_tx, f_mhz, d_km, h_gw, h_tx, environment):
    L_urban = okumura_hata_urban(f_mhz, d_km, h_gw, h_tx)

    if environment == "urban":
        path_loss = L_urban
    else:
        path_loss = okumura_hata_suburban(L_urban, f_mhz)

    ESP = P_tx - path_loss
    return ESP

ESP = compute_esp(
    P_TX,
    F_MHZ,
    distance_km,
    GW_HEIGHT,
    TX_HEIGHT,
    environment
)
print("\n==========  RESULT ==========")
print("Environment :", environment.upper())
print("Distance (km):", round(distance_km, 3))
print("Predicted ESP (dBm):", round(ESP, 2))
print("==================================")