import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path(__file__).parent / "coimbatore_satellite_samples.csv"
df = pd.read_csv(DATA_FILE)

print("DATA-DRIVEN URBAN GREEN COVER AND TEMPERATURE ANALYSIS")
print("Source: Landsat 8 satellite sample exported from Google Earth Engine")
print("Image date:", ", ".join(df["image_date"].dropna().astype(str).unique()))
print("\nFirst five rows:")
print(df.head().to_string(index=False))
print("\nSummary statistics:")
print(df[["NDVI", "Surface_Temperature_C"]].describe().round(3))
print("\nMean surface temperature by green-cover category:")
df["Green_Cover_Category"] = pd.cut(df["NDVI"], bins=[-1.01, 0.30, 0.50, 1.01], labels=["Low", "Medium", "High"], include_lowest=True)
print(df.groupby("Green_Cover_Category", observed=False)["Surface_Temperature_C"].mean().round(2))
print("\nPearson correlation:", round(df["NDVI"].corr(df["Surface_Temperature_C"]), 3))

plt.figure()
plt.scatter(df["NDVI"], df["Surface_Temperature_C"])
plt.xlabel("NDVI (vegetation greenness)")
plt.ylabel("Surface temperature (°C)")
plt.title("Coimbatore NDVI and Surface Temperature (7 Feb 2024)")
plt.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig(Path(__file__).parent / "ndvi_temperature_scatter.png", dpi=150)
print("\nSaved graph: ndvi_temperature_scatter.png")
