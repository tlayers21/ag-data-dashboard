# Agricultural Commodity Data Dashboard

A fully automated analytics platform for exploring USDA supply‑demand data across major U.S. agricultural commodities.

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

### Interactive Dashboard
- Built with **React**, **React Router**, and **Plotly**
- Commodity-specific pages for:
  - Corn
  - Wheat
  - Soybeans
  - Soybean Meal
  - Soybean Oil
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
- PostgreSQL
- Pandas
- Automated ETL pipeline
- Chart and Commentary generation engine

**Frontend**

- React
- React Router
- Plotly.js
- Custom UI components

---

## USDA Data Attribution

Data sourced from the USDA Foreign Agricultural Service (FAS) Open Data Portal:  
[https://apps.fas.usda.gov/opendatawebV2/#/](https://apps.fas.usda.gov/opendatawebV2/#/)

---

## Future Improvements

- Additional commodities
- More countries
- Forecasting
- Ethanol and other biofuels using an EIA API
- More years of past data