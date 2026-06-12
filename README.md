# Mumbai Crime Area Detector

A browser-based analytics dashboard providing ward-level crime intelligence across all 24 Brihanmumbai Municipal Corporation (BMC) wards. The application covers 10 crime categories spanning 2020–2024 and produces data-driven 2025 projections using linear regression. No installation is required — the dashboard runs entirely in a web browser.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Wards Covered](#wards-covered)
- [Crime Categories](#crime-categories)
- [Forecast Methodology](#forecast-methodology)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Interactive Bubble Map** — Colour-coded safety scores and crime volume visualised across all 24 wards; click any marker to open a detailed ward profile.
- **Ward Detail Panel** — Displays a safety score (0–100), per-crime-type breakdown with percentage bars, a mini trend sparkline, and a 2025 forecast range.
- **2025 Predictions** — Ordinary Least Squares linear regression with 95% confidence intervals presented as a readable low–high range.
- **Crime Heatmap** — A 24-ward × 10-crime-type matrix that instantly surfaces geographic and categorical hotspots.
- **Safety Rankings** — A full ward leaderboard from safest to riskiest, accompanied by a city-average gauge.
- **City Overview** — Zone-wise crime distribution, a crime-type donut chart, and year-over-year trend lines for the full city.
- **Multi-Entry Selection** — Ward selection via map click, dropdown search, or the KPI card Explore button.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | Streamlit >= 1.31 |
| Visualisation | Plotly 5.18 |
| Data Processing | pandas, NumPy |
| Forecasting | OLS Linear Regression (numpy.polyfit) |
| Map | Plotly go.Scattermapbox + Carto Positron |
| Deployment | Streamlit Cloud |

---

## Getting Started

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/mumbai-crime-detector.git
cd mumbai-crime-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### Requirements

```
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly==5.18.0
```

### Deploy on Streamlit Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repository, and set the main file to `app.py`.
4. Click **Deploy** — a public URL will be ready within approximately two minutes.

---

## Project Structure

```
mumbai-crime-detector/
│
├── app.py            # Main application — all logic, charts, and UI
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Wards Covered

The dashboard covers all 24 BMC municipal wards across seven policing zones.

| Zone | Wards |
|---|---|
| Zone I — South | A (Colaba), B (Mazgaon), D (Malabar Hill) |
| Zone II — Central | C, E, F/N, F/S, G/N, G/S |
| Zone III — Western Suburbs | H/E, H/W (Bandra) |
| Zone IV — Western Suburbs North | K/E, K/W (Andheri), P/N, P/S (Goregaon) |
| Zone V — Eastern Suburbs | L (Kurla), M/E, M/W, N (Ghatkopar) |
| Zone VI — North | R/C, R/N, R/S (Borivali) |
| Zone VII — North East | S (Bhandup), T (Mulund) |

---

## Crime Categories

Theft, Vehicle Theft, Robbery, Burglary, Assault, Murder, Kidnapping, Fraud, Drug Offences, Eve Teasing

---

## Forecast Methodology

For each ward, the application fits an Ordinary Least Squares linear regression on five annual data points (2020–2024) using `numpy.polyfit`. The full prediction standard error is computed as follows:

```
SE_pred = SE_residual × sqrt(1 + 1/n + (2025 − mean_year)² / Σ(year − mean_year)²)
```

Multiplying by 2 yields an approximate 95% confidence interval, displayed as a plain low–high range for readability.

---

## Roadmap

- Live data integration with the Mumbai Police Open Data API and NCRB feeds
- SARIMA and Prophet models to capture seasonal crime patterns
- PostgreSQL backend for large-scale historical data storage
- Mobile-optimised responsive layout
- Hindi and Marathi language localisation
- One-click PDF ward report export
- Authentication layer for law enforcement internal use

---

## Disclaimer

The crime data used in this application is synthetically generated using Poisson distributions calibrated against publicly available ward-level patterns. It is intended for educational and demonstration purposes only and does not represent official Mumbai Police or government statistics. No inferences about real crime rates or individual ward safety should be drawn from this data.

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it in accordance with the licence terms.

---

## Acknowledgements

- [Streamlit](https://streamlit.io) — for the rapid application framework
- [Plotly](https://plotly.com) — for interactive charts and map rendering
- [Carto](https://carto.com) — for the Positron basemap tiles (no API key required)
- Mumbai Police and BMC — for publicly available ward boundary and zoning reference data
