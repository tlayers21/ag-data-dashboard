import React from "react";
import "./About.css";

function DataOverview() {
  return (
    <div className="about-page">
      <div className="about-card">
        <h2>Data Overview</h2>

        <table className="learn-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Field</th>
              <th>Definition</th>
            </tr>
          </thead>

          <tbody>

            {/* ESR */}
            <tr>
              <td rowSpan="8"><strong>Export Sales Report (ESR)</strong></td>
              <td>Weekly Exports</td>
              <td>Exports shipped during the current reporting week.</td>
            </tr>
            <tr>
              <td>Accumulated Exports</td>
              <td>Total exports shipped so far in the marketing year.</td>
            </tr>
            <tr>
              <td>Outstanding Sales</td>
              <td>Sales made but not yet shipped.</td>
            </tr>
            <tr>
              <td>Gross New Sales</td>
              <td>Total new sales before cancellations.</td>
            </tr>
            <tr>
              <td>Current Marketing Year Net Sales</td>
              <td>New sales minus cancellations for the current marketing year.</td>
            </tr>
            <tr>
              <td>Current Marketing Year Total Commitment</td>
              <td>Accumulated exports plus outstanding sales.</td>
            </tr>
            <tr>
              <td>Next Marketing Year Outstanding Sales</td>
              <td>Sales for next marketing year not yet shipped.</td>
            </tr>
            <tr>
              <td>Next Marketing Year Net Sales</td>
              <td>Net new sales for the next marketing year.</td>
            </tr>

            {/* PSD */}
            <tr>
              <td rowSpan="21"><strong>Production, Supply, and Distribution (PSD)</strong></td>
              <td>Area Harvested</td>
              <td>Total land area harvested for the crop.</td>
            </tr>
            <tr>
              <td>Crush</td>
              <td>Volume of raw commodity processed (e.g., soybeans crushed).</td>
            </tr>
            <tr>
              <td>Beginning Stocks</td>
              <td>Inventory available at the start of the marketing year.</td>
            </tr>
            <tr>
              <td>Production</td>
              <td>Total output produced during the year.</td>
            </tr>
            <tr>
              <td>Imports</td>
              <td>Commodity brought into the country.</td>
            </tr>
            <tr>
              <td>Trade Year Imports</td>
              <td>Imports measured on a trade‑year basis <em>(trade year: period where trade activity is tracked for a given commodity, differs from marketing year).</em></td>
            </tr>
            <tr>
              <td>Trade Year Imports From United States</td>
              <td>Imports sourced specifically from the U.S.  <em>(appears to not have been updated for the 2024/2025 marketing year yet as of early 2026).</em></td>
            </tr>
            <tr>
              <td>Total Supply</td>
              <td>Beginning stocks + production + imports.</td>
            </tr>
            <tr>
              <td>Exports</td>
              <td>Total shipments leaving the country.</td>
            </tr>
            <tr>
              <td>Trade Year Exports</td>
              <td>Exports measured on a trade‑year basis.</td>
            </tr>
            <tr>
              <td>Domestic Consumption</td>
              <td>Total use within the country.</td>
            </tr>
            <tr>
              <td>Feed Domestic Consumption</td>
              <td>Use of the commodity in animal feed.</td>
            </tr>
            <tr>
              <td>Industrial Domestic Consumption</td>
              <td>Use in industrial processes (ethanol, biodiesel, etc.).</td>
            </tr>
            <tr>
              <td>Food Use Domestic Consumption</td>
              <td>Use in food products for human consumption.</td>
            </tr>
            <tr>
              <td>Feed Waste Domestic Consumption</td>
              <td>Losses or waste in feed channels.</td>
            </tr>
            <tr>
              <td>Ending Stocks</td>
              <td>Inventory remaining at the end of the marketing year.</td>
            </tr>
            <tr>
              <td>Total Distribution</td>
              <td>Total supply allocated across all uses <em>(must = total supply).</em></td>
            </tr>
            <tr>
              <td>Extraction Rate</td>
              <td>Yield of processed product per unit of raw commodity.</td>
            </tr>
            <tr>
              <td>Yield</td>
              <td>Production per unit of harvested area.</td>
            </tr>
            <tr>
              <td>Food Seed and Industrial Consumption</td>
              <td>Combined use for food, seed, and industrial purposes.</td>
            </tr>
            <tr>
              <td>Soybean Meal Equivalent</td>
              <td>Converted volume expressed in soybean meal terms.</td>
            </tr>

            {/* Inspections */}
            <tr>
              <td><strong>Weekly Export Inspections</strong></td>
              <td>Export Inspections</td>
              <td>Physical inspections of shipments prior to export.</td>
            </tr>

          </tbody>
        </table>

        <p style={{ marginTop: "1rem", fontSize: "0.9rem", textAlign: "center" }}>
          For more information about the underlying datasets, visit the{" "}
          <a
            href="https://apps.fas.usda.gov/opendatawebV2/#/"
            target="_blank"
            rel="noopener noreferrer"
          >
            USDA FAS Open Data Portal
          </a>.
        </p>
      </div>
    </div>
  );
}

export default DataOverview;