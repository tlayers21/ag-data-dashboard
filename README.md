# Agricultural Commodity Data Dashboard

A fully automated analytics platform for exploring USDA export and supply‑demand data across major U.S. agricultural commodities.

---

## Overview

This project provides a unified, modern interface for analyzing key USDA datasets used across commodity markets. It integrates three major data sources:

- **Export Sales Reporting (ESR)**
- **Production, Supply, and Distribution (PSD)**
- **Export Inspections**

The platform automatically fetches, cleans, stores, and visualizes these datasets, updating charts and commentary daily and accommodating new USDA releases as they occur.

The frontend is a **React-based dashboard** designed for clarity, speed, and ease of use. Users can explore commodities, switch between data sources, compare countries, and view multi-year historical trends.

---

## Features

### Automated Data Pipeline
- Fetches ESR and PSD data directly from the USDA FAS Open Data APIs
- Parses historical Export Inspections reports
- Cleans, normalizes, and stores all data in a SQL database
- Generates charts and homepage summaries automatically
- Runs on a scheduled basis with a maintenance-mode flag for safe updates

### Interactive Dashboard
- Built with **React**, **React Router**, and **Plotly**
- Commodity-specific pages for:
  - Corn
  - Wheat (including SRW & HRW)
  - Soybeans
  - Soybean Meal
  - Soybean Oil
  - Ethanol
- Dynamic chart rendering with multiple data sources
- Country and metric selectors
- Clean, mobile-friendly layout

### Data Overview Page
- A dedicated page explaining all ESR, PSD, and Inspections fields
- Clear definitions with professional table layout

---

## Data Sources

### Export Sales Reporting (ESR)
Fetched via USDA FAS Open Data API. Includes metrics such as:

- Weekly Exports
- Accumulated Exports
- Outstanding Sales
- Gross New Sales
- Current & Next Marketing Year Net Sales
- Total Commitments

### Production, Supply & Distribution (PSD)
Fetched via USDA API. Includes:

- Area Harvested
- Production
- Imports / Exports
- Domestic Consumption
- Ending Stocks
- Yield
- Industrial Use
- Food/Seed/Industrial Consumption
- Soybean Meal Equivalent
- …and more

### Export Inspections
- Parsed from historical USDA inspection reports
- Normalized into a consistent structure

---

## Tech Stack

**Backend**

- FastAPI
- SQLAlchemy
- Pandas
- Automated ETL pipeline
- Maintenance-mode flag system
- Chart generation engine

**Frontend**

- React
- React Router
- Plotly.js
- Custom UI components
- Mobile-friendly table wrappers

---

## Maintenance Mode

During automated updates, the backend creates a `maintenance.flag` file.  
The frontend checks `/maintenance` on load and redirects users to a clean **“System Updating”** page until the pipeline finishes.  

This ensures:

- No partial data loads
- No broken charts
- No inconsistent states

---

## 👤 About the Developer

**Thomas Ayers**  
Undergraduate at Virginia Tech  

- **Major:** Computer Science  
- **Minors:** Mathematics & Commodity Market Analytics  
- **Member of COINS** (Commodity Investing by Students), a student-run commodity trading group focused on futures-based ETF strategies  

This project was built to give the COINS agriculture division — and anyone interested in commodity markets — a fast, intuitive way to access and analyze USDA data without digging through spreadsheets or raw APIs.

**📬 Contact**

- Email: [tlayers21@gmail.com](mailto:tlayers21@gmail.com)  
- Phone: (571) 510‑5440  
- LinkedIn: [https://www.linkedin.com/in/thomas-l-ayers](https://www.linkedin.com/in/thomas-l-ayers)

---

## USDA Data Attribution

Data sourced from the USDA Foreign Agricultural Service (FAS) Open Data Portal:  
[https://apps.fas.usda.gov/opendatawebV2/#/](https://apps.fas.usda.gov/opendatawebV2/#/)

---

## Future Improvements

- Additional commodities
- More Countries
- Forecasting
- Ethanol and other biofuels using an EIA API
- More years of data