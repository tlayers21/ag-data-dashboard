import { useEffect, useState } from "react";
import ChartViewer from "../components/ChartViewer";

// CORN FILES
import cornInspect from "../commentary/us_corn_to_world_export_inspections_commentary.txt";
import cornCommit from "../commentary/us_corn_to_world_current_marketing_year_total_commitment_commentary.txt";
import cornSales from "../commentary/us_corn_to_world_gross_new_sales_commentary.txt";
import cornNextMY from "../commentary/us_corn_to_world_next_marketing_year_outstanding_sales_commentary.txt";

// WHEAT FILES
import wheatInspect from "../commentary/us_wheat_to_world_export_inspections_commentary.txt";
import wheatCommit from "../commentary/us_wheat_to_world_current_marketing_year_total_commitment_commentary.txt";
import wheatSales from "../commentary/us_wheat_to_world_gross_new_sales_commentary.txt";
import wheatNextMY from "../commentary/us_wheat_to_world_next_marketing_year_outstanding_sales_commentary.txt";

// SOYBEAN FILES
import soyInspect from "../commentary/us_soybeans_to_world_export_inspections_commentary.txt";
import soyCommit from "../commentary/us_soybeans_to_world_current_marketing_year_total_commitment_commentary.txt";
import soySales from "../commentary/us_soybeans_to_world_gross_new_sales_commentary.txt";
import soyNextMY from "../commentary/us_soybeans_to_world_next_marketing_year_outstanding_sales_commentary.txt";

// Remove date for non-inspection files
function stripDate(text) {
  return text.replace(/^[A-Z]{3}-\d{1,2}:\s*/g, "");
}

// Bold date for inspections
function boldDate(text) {
  return text.replace(
    /^([A-Z]{3}-\d{1,2}:)/,
    "<strong>$1</strong> "
  );
}

async function combineCommodity(files) {
  const [inspect, commit, sales, nextMY] = await Promise.all(
    files.map((f) => fetch(f).then((r) => r.text()))
  );

  // Bold date for inspections
  const part1 = inspect.trim().replace(
    /^([A-Z]{3}-\d{1,2}:)/,
    "<strong>$1</strong>"
  );

  // Remove date for all others
  const part2 = commit.trim().replace(/^[A-Z]{3}-\d{1,2}:\s*/g, "");
  const part3 = sales.trim().replace(/^[A-Z]{3}-\d{1,2}:\s*/g, "");
  const part4 = nextMY.trim().replace(/^[A-Z]{3}-\d{1,2}:\s*/g, "");

  // Join into ONE paragraph
  return [part1, part2, part3, part4].join(" ");
}

export default function Home() {
  const [cornCommentary, setCornCommentary] = useState("");
  const [wheatCommentary, setWheatCommentary] = useState("");
  const [soyCommentary, setSoyCommentary] = useState("");

  useEffect(() => {
    async function loadAll() {
      setCornCommentary(
        await combineCommodity([
          cornInspect,
          cornCommit,
          cornSales,
          cornNextMY
        ])
      );

      setWheatCommentary(
        await combineCommodity([
          wheatInspect,
          wheatCommit,
          wheatSales,
          wheatNextMY
        ])
      );

      setSoyCommentary(
        await combineCommodity([
          soyInspect,
          soyCommit,
          soySales,
          soyNextMY
        ])
      );
    }

    loadAll();
  }, []);

  return (
    <div className="main-content">

      {/* CORN SECTION */}
      <h2>Recent Corn Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer jsonPath="/us_corn_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_corn_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/us_corn_to_world_gross_new_sales_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_corn_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* CORN COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: cornCommentary }}
        />
      </div>

      {/* WHEAT SECTION */}
      <h2 style={{ marginTop: "3rem" }}>Recent Wheat Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_gross_new_sales_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_wheat_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* WHEAT COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: wheatCommentary }}
        />
      </div>

      {/* SOYBEAN SECTION */}
      <h2 style={{ marginTop: "3rem" }}>Recent Soybean Charts</h2>

      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_inspections_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Current Marketing Year Total Commitment</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_current_marketing_year_total_commitment_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_gross_new_sales_last_5_years_my.json" />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer jsonPath="/us_soybeans_to_world_next_marketing_year_outstanding_sales_last_5_years_my.json" />
        </div>
      </div>

      {/* SOYBEAN COMMENTARY */}
      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: soyCommentary }}
        />
      </div>

    </div>
  );
}