import "./About.css";

const SECTIONS = [
  {
    type: "Export Sales Report (ESR)",
    fields: [
      ["Weekly Exports", "Exports shipped during the current reporting week."],
      ["Accumulated Exports", "Total exports shipped so far in the marketing year."],
      ["Outstanding Sales", "Sales made but not yet shipped."],
      ["Gross New Sales", "Total new sales before cancellations."],
      ["Current Marketing Year Net Sales", "New sales minus cancellations for the current marketing year."],
      ["Current Marketing Year Total Commitment", "Accumulated exports plus outstanding sales."],
      ["Next Marketing Year Outstanding Sales", "Sales for next marketing year not yet shipped."],
      ["Next Marketing Year Net Sales", "Net new sales for the next marketing year."]
    ]
  },
  {
    type: "Production, Supply, and Distribution (PSD)",
    fields: [
      ["Area Harvested", "Total land area harvested for the crop."],
      ["Crush", "Volume of raw commodity processed (e.g., soybeans crushed)."],
      ["Beginning Stocks", "Inventory available at the start of the marketing year."],
      ["Production", "Total output produced during the year."],
      ["Imports", "Commodity brought into the country."],
      ["Trade Year Imports", <>Imports measured on a trade‑year basis <em>(trade year: period where trade activity is tracked for a given commodity, differs from marketing year).</em></>],
      ["Trade Year Imports From United States", <>Imports sourced specifically from the U.S.  <em>(appears to not have been updated for the 2024/2025 marketing year yet as of early 2026).</em></>],
      ["Total Supply", "Beginning stocks + production + imports."],
      ["Exports", "Total shipments leaving the country."],
      ["Trade Year Exports", "Exports measured on a trade‑year basis."],
      ["Domestic Consumption", "Total use within the country."],
      ["Feed Domestic Consumption", "Use of the commodity in animal feed."],
      ["Industrial Domestic Consumption", "Use in industrial processes (ethanol, biodiesel, etc.)."],
      ["Food Use Domestic Consumption", "Use in food products for human consumption."],
      ["Feed Waste Domestic Consumption", "Losses or waste in feed channels."],
      ["Ending Stocks", "Inventory remaining at the end of the marketing year."],
      ["Total Distribution", <>Total supply allocated across all uses <em>(must = total supply).</em></>],
      ["Extraction Rate", "Yield of processed product per unit of raw commodity."],
      ["Yield", "Production per unit of harvested area."],
      ["Food Seed and Industrial Consumption", "Combined use for food, seed, and industrial purposes."],
      ["Soybean Meal Equivalent", "Converted volume expressed in soybean meal terms."]
    ]
  },
  {
    type: "Weekly Export Inspections",
    fields: [["Export Inspections", "Physical inspections of shipments prior to export."]]
  }
];

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
            {SECTIONS.flatMap(({ type, fields }) =>
              fields.map(([field, definition], i) => (
                <tr key={field}>
                  {i === 0 && (
                    <td rowSpan={fields.length}><strong>{type}</strong></td>
                  )}
                  <td>{field}</td>
                  <td>{definition}</td>
                </tr>
              ))
            )}
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
