import Card from "../components/Card";
import ChartViewer from "../components/ChartViewer";

export default function Home() {
  return (
    <div className="main-content">

      {/* CORN SECTION */}
      <h2>Recent Corn Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Weekly Inspections</h3>
          <ChartViewer jsonPath="/us_corn_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Weekly Exports</h3>
          <ChartViewer jsonPath="/us_corn_to_world_weekly_exports_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_corn_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_corn_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* CORN COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <p>
          Export flows showed a mild uptick compared to the prior five‑year pattern,
          with inspections drifting sideways while weekly shipments bounced around
          typical seasonal ranges. Buyers remained active but uneven, and forward
          sales hinted at a slightly firmer tone than earlier in the quarter. Nothing
          dramatic, but enough movement to keep the market attentive.
        </p>
      </div>


      {/* WHEAT SECTION */}
      <h2 style={{ marginTop: "3rem" }}>Recent Wheat Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Weekly Inspections</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Weekly Exports</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_weekly_exports_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* WHEAT COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <p>
          Export flows showed a mild uptick compared to the prior five‑year pattern,
          with inspections drifting sideways while weekly shipments bounced around
          typical seasonal ranges. Buyers remained active but uneven, and forward
          sales hinted at a slightly firmer tone than earlier in the quarter. Nothing
          dramatic, but enough movement to keep the market attentive.
        </p>
      </div>


      {/* SOYBEAN SECTION */}
      <h2 style={{ marginTop: "3rem" }}>Recent Soybean Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Weekly Inspections</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Weekly Exports</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_weekly_exports_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* SOYBEAN COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <p>
          Export flows showed a mild uptick compared to the prior five‑year pattern,
          with inspections drifting sideways while weekly shipments bounced around
          typical seasonal ranges. Buyers remained active but uneven, and forward
          sales hinted at a slightly firmer tone than earlier in the quarter. Nothing
          dramatic, but enough movement to keep the market attentive.
        </p>
      </div>

    </div>
  );
}