# Urban Green Cover and Temperature Analysis

## Data source and limitation
The included `coimbatore_satellite_samples.csv` contains 20 valid sample points exported from Google Earth Engine using Landsat 8 Collection 2 Level-2 imagery. The selected image date is 2024-02-07. It is real satellite-derived sample data, but represents one image date and the sampled points only; do not describe it as a year-round trend or as ground-station air temperature.

The CSV columns are longitude, latitude, NDVI, Surface_Temperature_C, and image_date. NDVI was calculated using scaled Landsat surface reflectance bands. Surface temperature was converted from the Landsat ST_B10 scale to Celsius.

## Files
- `app.py`: interactive Streamlit dashboard
- `analysis.py`: standalone Python analysis and graph creation
- `coimbatore_satellite_samples.csv`: exported satellite sample dataset
- `requirements.txt`: required Python packages
- `Project_Report_Draft.docx`: report starter draft; update the results section with the measured results before submission

## Run on Windows
1. Open Command Prompt in this folder.
2. Install dependencies: `py -m pip install -r requirements.txt`
3. Run analysis: `py analysis.py`
4. Start dashboard: `py -m streamlit run app.py`
5. Open the local URL shown in Command Prompt (normally http://localhost:8501).

## Method
The dashboard previews the sample data, calculates descriptive statistics and Pearson correlation, and plots NDVI against land surface temperature. It also compares average surface temperature across low, medium, and high NDVI categories. Correlation indicates association, not causation.
