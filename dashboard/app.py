import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Setup
st.set_page_config(
    page_title="Corn Exports Dashboard", 
    layout="wide"
)

st.title("U.S. Corn Exports 2025 Analysis")

# Load some data
processed_path = Path("../data/processed/corn_exports_2025.csv")
weekly_data = pd.read_csv(processed_path, parse_dates=["date"])

total_exports = weekly_data["weekly_exports_mt"].sum()
avg_weekly = weekly_data["weekly_exports_mt"].mean()
peak_week = weekly_data.loc[weekly_data["weekly_exports_mt"].idxmax()]

# Add some information
col1, col2, col3 = st.columns(3)
col1.metric("Total Exports (MT)", f"{total_exports:,.0f}")
col2.metric("Average Weekly Exports (MT)", f"{avg_weekly:,.0f}")
col3.metric("Peak Week", peak_week["date"].strftime("%b %d, %Y"))

# Add some pictures
figure1 = px.line(
    weekly_data,
    x="date",
    y=["weekly_exports_mt", "moving_average_4w"],
    title="Weekly Corn Exports (2025)",
    markers=True,
    labels={
        "date": "Week Ending Date",
        "weekly_exports_mt": "Exports (MT)",
        "moving_average_4w": "4-Week Moving Average (MT)"
    }
)

figure1.for_each_trace(lambda t: t.update(name="Exports (MT)" if t.name=="weekly_exports_mt" else "4-week Moving Average (MT)"))
figure1.update_layout(legend_title_text="Series")
figure1.update_yaxes(title_text="Exports (MT)")
st.plotly_chart(figure1, width="stretch")

figure2 = px.line(
    weekly_data,
    x="date",
    y="std_4w",
    title="Weekly Corn Exports Volatility",
    markers=True,
    labels={
        "date": "Week Ending Date",
        "std_4w": "Exports (MT)"
    }
)

figure2.update_traces(line_color="green")
st.plotly_chart(figure2, width="stretch")

# Add commentary
commentary_path = Path("../data/processed/corn_exports_2025_commentary.txt")
with open(commentary_path, "r") as f:
    commentary = f.read()
commentary = commentary.replace("\n", " ")
st.subheader("Commentary:")
st.write(commentary)