import { useEffect, useState } from "react";
import ChartViewer from "../components/ChartViewer";

export default function Home() {
  const [commentary, setCommentary] = useState("");

  // API = backend/api
  const API = process.env.REACT_APP_API_BASE;

  // ROOT = backend root (no /api)
  const ROOT = API.replace("/api", "");

  useEffect(() => {
    async function load() {
      const res = await fetch(`${ROOT}/commentary/home`);
      let text = await res.text();

      // Split into lines
      let lines = text.split("\n").filter(Boolean);

      if (lines.length > 0) {
        // Bold the first date prefix
        lines[0] = lines[0].replace(
          /^([A-Z]{3}-\d{1,2}:)/,
          "<strong>$1</strong>"
        );

        // Strip date prefixes from all other lines
        for (let i = 1; i < lines.length; i++) {
          lines[i] = lines[i].replace(/^[A-Z]{3}-\d{1,2}:\s*/, "");
        }
      }

      setCommentary(lines.join(" "));
    }

    load();
  }, [ROOT]);

  return (
    <div className="main-content">

      {/* ============================
          CORN SECTION
      ============================ */}
      <h2>Recent Corn Charts</h2>

      <div className="card-grid-2">

        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/inspections/world/export_inspections/my`}
          />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/current_marketing_year_total_commitment/my`}
          />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/gross_new_sales/my`}
          />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/next_marketing_year_outstanding_sales/my`}
          />
        </div>

      </div>

      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: commentary }}
        />
      </div>


      {/* ============================
          WHEAT SECTION
      ============================ */}
      <h2 style={{ marginTop: "3rem" }}>Recent Wheat Charts</h2>

      <div className="card-grid-2">

        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/inspections/world/export_inspections/my`}
          />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/current_marketing_year_total_commitment/my`}
          />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/gross_new_sales/my`}
          />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/next_marketing_year_outstanding_sales/my`}
          />
        </div>

      </div>

      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: commentary }}
        />
      </div>


      {/* ============================
          SOYBEANS SECTION
      ============================ */}
      <h2 style={{ marginTop: "3rem" }}>Recent Soybean Charts</h2>

      <div className="card-grid-2">

        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/inspections/world/export_inspections/my`}
          />
        </div>

        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/current_marketing_year_total_commitment/my`}
          />
        </div>

        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/gross_new_sales/my`}
          />
        </div>

        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/next_marketing_year_outstanding_sales/my`}
          />
        </div>

      </div>

      <div className="commentary-box">
        <h3>Commentary:</h3>
        <div
          style={{ whiteSpace: "pre-line" }}
          dangerouslySetInnerHTML={{ __html: commentary }}
        />
      </div>

    </div>
  );
}