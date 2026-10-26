import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Urban Green Cover & Temperature", page_icon="🌳", layout="wide")
st.title("🌳 Data-Driven Urban Green Cover and Temperature Analysis")
st.caption("Coimbatore, Tamil Nadu | Landsat 8 satellite sample | Image date: 7 February 2024")

DATA_FILE = Path(__file__).parent / "coimbatore_satellite_samples.csv"
uploaded = st.sidebar.file_uploader("Upload another CSV (optional)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    data_source = "Uploaded CSV"
else:
    df = pd.read_csv(DATA_FILE)
    data_source = "Landsat 8 satellite samples exported from Google Earth Engine"

required = {"NDVI", "Surface_Temperature_C"}
missing = required - set(df.columns)
if missing:
    st.error("CSV is missing required columns: " + ", ".join(sorted(missing)))
    st.info("Required columns: NDVI, Surface_Temperature_C. Coordinate columns are recommended.")
    st.stop()

for col in ["NDVI", "Surface_Temperature_C", "longitude", "latitude"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["NDVI", "Surface_Temperature_C"])
df = df[(df["NDVI"] >= -1) & (df["NDVI"] <= 1)]
if df.empty:
    st.error("No valid rows found. Check the NDVI and temperature values in your CSV.")
    st.stop()

if "Location" not in df.columns:
    if {"longitude", "latitude"}.issubset(df.columns):
        df["Location"] = df.apply(lambda r: f"({r['latitude']:.2f}, {r['longitude']:.2f})", axis=1)
    else:
        df["Location"] = [f"Sample {i+1}" for i in range(len(df))]
if "image_date" in df.columns:
    dates = ", ".join(sorted(df["image_date"].dropna().astype(str).unique()))
    st.caption(f"Satellite image date(s): {dates}")
st.info(f"Data source: **{data_source}**. This dataset represents one satellite image date; it is not a year-round trend.")

st.subheader("Dataset preview")
st.dataframe(df, use_container_width=True)
c1, c2, c3 = st.columns(3)
c1.metric("Valid sample points", f"{len(df)}")
c2.metric("Mean NDVI", f"{df['NDVI'].mean():.3f}")
c3.metric("Mean surface temperature", f"{df['Surface_Temperature_C'].mean():.2f} °C")

st.subheader("Explore the data")
min_ndvi, max_ndvi = float(df["NDVI"].min()), float(df["NDVI"].max())
if min_ndvi < max_ndvi:
    selected_range = st.slider("Filter by NDVI (vegetation greenness)", min_value=min_ndvi, max_value=max_ndvi, value=(min_ndvi, max_ndvi))
    filtered = df[df["NDVI"].between(selected_range[0], selected_range[1])].copy()
else:
    filtered = df.copy()
st.write(f"Sample points in selected range: **{len(filtered)}**")
filtered["Green_Cover_Category"] = pd.cut(filtered["NDVI"], bins=[-1.01, 0.30, 0.50, 1.01], labels=["Low", "Medium", "High"], include_lowest=True).astype(str)
left, right = st.columns(2)
with left:
    st.markdown("**Vegetation greenness vs. surface temperature**")
    fig, ax = plt.subplots()
    ax.scatter(filtered["NDVI"], filtered["Surface_Temperature_C"])
    ax.set_xlabel("NDVI (vegetation greenness)")
    ax.set_ylabel("Surface temperature (°C)")
    ax.set_title("NDVI and surface temperature")
    ax.grid(True, alpha=0.25)
    st.pyplot(fig)
    plt.close(fig)
with right:
    st.markdown("**Average temperature by green-cover category**")
    grouped = filtered.groupby("Green_Cover_Category", observed=False)["Surface_Temperature_C"].mean().dropna()
    fig2, ax2 = plt.subplots()
    grouped.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Green-cover category")
    ax2.set_ylabel("Mean surface temperature (°C)")
    ax2.set_title("Average temperature by category")
    ax2.tick_params(axis="x", rotation=0)
    ax2.grid(axis="y", alpha=0.25)
    st.pyplot(fig2)
    plt.close(fig2)

st.subheader("Summary statistics")
st.dataframe(filtered[["NDVI", "Surface_Temperature_C"]].describe().round(3), use_container_width=True)
if len(filtered) >= 2 and filtered["NDVI"].nunique() > 1 and filtered["Surface_Temperature_C"].nunique() > 1:
    corr = filtered["NDVI"].corr(filtered["Surface_Temperature_C"])
    st.metric("Pearson correlation (NDVI vs. temperature)", f"{corr:.3f}")
    if corr < -0.3:
        st.write("In these sample points, higher NDVI tends to be associated with lower surface temperature.")
    elif corr > 0.3:
        st.write("In these sample points, higher NDVI tends to be associated with higher surface temperature.")
    else:
        st.write("In these sample points, the linear association appears weak.")
    st.caption("Correlation does not prove causation. Results depend on image date, sample coverage, scale, and local factors.")
else:
    st.warning("At least two varied observations are needed to calculate correlation.")
st.download_button("Download filtered data as CSV", data=filtered.to_csv(index=False).encode("utf-8"), file_name="filtered_coimbatore_satellite_samples.csv", mime="text/csv")
st.caption("Source: Landsat 8 Collection 2 Level-2, sampled in Google Earth Engine. Surface temperature was converted from the ST_B10 scale to Celsius; NDVI was calculated from scaled surface reflectance bands.")
