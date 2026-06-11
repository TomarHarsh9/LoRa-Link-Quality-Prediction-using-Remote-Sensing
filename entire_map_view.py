import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

with rasterio.open("landcover_map.tif") as src:
    landcover = src.read(1)

colors = ["red", "gray", "green", "blue", "brown"]
cmap = ListedColormap(colors)

plt.figure(figsize=(6,6))
plt.imshow(landcover, cmap=cmap)
plt.colorbar(ticks=[0,1,2,3,4])
plt.title("Land-cover classification")
plt.show()
