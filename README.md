# mumbai_crime_detector
📌 Overview
The Mumbai Crime Area Detector is a browser-based analytics dashboard that brings ward-level crime data for all 24 Brihanmumbai Municipal Corporation (BMC) wards into a single, interactive interface. It covers 10 crime categories across the period 2020–2024 and generates data-driven 2025 predictions using linear regression.
Designed for citizens, researchers, urban planners, and policy analysts, the app requires no installation — just open it in a browser.

✨ Features

🗺 Interactive bubble map — colour-coded safety scores and crime volume for all 24 wards; click any marker to drill in
📊 Ward detail panel — safety score (0–100), crime breakdown bars with percentages, mini trend sparkline, and 2025 forecast
📈 2025 predictions — OLS linear regression with 95% confidence intervals shown as a human-readable range
🔥 Crime heatmap — 24 wards × 10 crime types, instantly revealing hotspots
🏆 Safety rankings — full safest/riskiest ward leaderboard with a city average gauge
🏙 City overview — zone-wise distribution, crime type donut chart, year-over-year trend lines
🔍 Multi-entry selection — select a ward via map click, dropdown search, or KPI card Explore button


🛠 Tech Stack
LayerToolFrameworkStreamlit >= 1.31VisualisationPlotly 5.18Data Processingpandas, NumPyForecastingOLS Linear Regression (numpy.polyfit)MapPlotly go.Scattermapbox + Carto PositronDeploymentStreamlit Cloud

🚀 Getting Started
Run locally
bash# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/mumbai-crime-detector.git
cd mumbai-crime-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
Then open http://localhost:8501 in your browser.
Requirements
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly==5.18.0

☁️ Deploy on Streamlit Cloud (Free)

Push this repo to GitHub
Go to share.streamlit.io and sign in with GitHub
Click New app → select your repo → set main file to app.py
Click Deploy — your public URL will be ready in ~2 minutes


📂 Project Structure
mumbai-crime-detector/
│
├── app.py               # Main application — all logic, charts, and UI
├── requirements.txt     # Python dependencies
└── README.md            # This file

🗺 Wards Covered
The dashboard covers all 24 BMC municipal wards across 7 policing zones:
ZoneWardsZone I – SouthA (Colaba), B (Mazgaon), D (Malabar Hill)Zone II – CentralC, E, F/N, F/S, G/N, G/SZone III – Western SuburbsH/E, H/W (Bandra)Zone IV – W Suburbs NorthK/E, K/W (Andheri), P/N, P/S (Goregaon)Zone V – Eastern SuburbsL (Kurla), M/E, M/W, N (Ghatkopar)Zone VI – NorthR/C, R/N, R/S (Borivali)Zone VII – North EastS (Bhandup), T (Mulund)

📊 Crime Categories
Theft · Vehicle Theft · Robbery · Burglary · Assault · Murder · Kidnapping · Fraud · Drug Offences · Eve Teasing

🔮 How the 2025 Forecast Works
For each ward, the app fits an Ordinary Least Squares linear regression on the 5 annual data points (2020–2024) using numpy.polyfit. It then computes the full prediction standard error:
SE_pred = SE_residual × sqrt(1 + 1/n + (2025 − mean_year)² / Σ(year − mean_year)²)
Multiplying by 2 gives the approximate 95% confidence interval, displayed as a plain low – high range rather than a ±value for readability.

🔭 Future Scope

🔗 Live data integration with Mumbai Police Open Data API / NCRB
📅 SARIMA / Prophet models to capture seasonal crime patterns
🗃 PostgreSQL backend for historical data at scale
📱 Mobile-optimised responsive layout
🌐 Hindi and Marathi language support
📄 One-click PDF ward report export
🔐 Authentication layer for law enforcement internal use


⚠️ Disclaimer
The crime data used in this application is synthetically generated using Poisson distributions calibrated against publicly available ward-level patterns. It is intended for educational and demonstration purposes only and does not represent official Mumbai Police statistics.

📄 License
This project is licensed under the MIT License — feel free to use, modify, and distribute.

🙏 Acknowledgements

Streamlit — for making data apps this fast to build
Plotly — for the interactive charts and map
Carto — for the Positron basemap tiles (no API key required)
Mumbai Police & BMC — for publicly available ward boundary and zoning data


<p align="center">
  Built with 🏙 for Mumbai &nbsp;·&nbsp; Streamlit · Plotly · pandas · NumPy
</p>
