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

async function combineCommodity(files) {
  const [inspect, commit, sales, nextMY] = await Promise.all(
    files.map((f) => fetch(f).then((r) => r.text()))
  );

  const part1 = inspect.trim().replace(
    /^([A-Z]{3}-\d{1,2}:)/,
    "<strong>$1</strong>"
  );

  const strip = (t) => t.trim().replace(/^[A-Z]{3}-\d{1,2}:\s*/g, "");

  return [part1, strip(commit), strip(sales), strip(nextMY)].join(" ");
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
          <ChartViewer jsonPath="/inspections_us_corn_to_world_export_inspections_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer jsonPath="/esr_us_corn_to_world_current_marketing_year_total_commitment_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/esr_us_corn_to_world_gross_new_sales_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Next MY Outstanding Sales</h3>
          <ChartViewer jsonPath="/esr_us_corn_to_world_next_marketing_year_outstanding_sales_last_5_years_my_home.json" />
        </div>
      </div>

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
          <ChartViewer jsonPath="/inspections_us_wheat_to_world_export_inspections_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer jsonPath="/esr_us_wheat_to_world_current_marketing_year_total_commitment_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/esr_us_wheat_to_world_gross_new_sales_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Next MY Outstanding Sales</h3>
          <ChartViewer jsonPath="/esr_us_wheat_to_world_next_marketing_year_outstanding_sales_last_5_years_my_home.json" />
        </div>
      </div>

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
          <ChartViewer jsonPath="/inspections_us_soybeans_to_world_export_inspections_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer jsonPath="/esr_us_soybeans_to_world_current_marketing_year_total_commitment_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer jsonPath="/esr_us_soybeans_to_world_gross_new_sales_last_5_years_my_home.json" />
        </div>

        <div className="card">
          <h3>Next MY Outstanding Sales</h3>
          <ChartViewer jsonPath="/esr_us_soybeans_to_world_next_marketing_year_outstanding_sales_last_5_years_my_home.json" />
        </div>
      </div>

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