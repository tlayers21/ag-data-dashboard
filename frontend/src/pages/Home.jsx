import { useEffect, useState } from "react";
import ChartViewer from "../components/ChartViewer";
import { loadCommentary } from "../utils/loadCommentary";

export default function Home() {
  const [loading, setLoading] = useState(true);

  const [cornCommentary, setCornCommentary] = useState("");
  const [wheatCommentary, setWheatCommentary] = useState("");
  const [soyCommentary, setSoyCommentary] = useState("");

  const API = process.env.REACT_APP_API_BASE;

  useEffect(() => {
    async function load() {
      const { corn, wheat, soybeans } = await loadCommentary();
      setCornCommentary(corn);
      setWheatCommentary(wheat);
      setSoyCommentary(soybeans);

      // Give Render time to wake up
      setTimeout(() => setLoading(false), 20000); // 20 seconds
    }
    load();
  }, []);

  // Loading overlay
  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="loader"></div>
        <p>Warming up the data engine…</p>
      </div>
    );
  }

  return (
    <div className="main-content">

      {/* CORN */}
      <h2>Recent Corn Charts</h2>
      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/inspections/world/export_inspections/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/current_marketing_year_total_commitment/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/gross_new_sales/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/corn/esr/world/next_marketing_year_outstanding_sales/my`}
            variant="home"
          />
        </div>
      </div>

      <div className="commentary-box">
        <h3>Corn Commentary:</h3>
        <div dangerouslySetInnerHTML={{ __html: cornCommentary }} />
      </div>

      {/* WHEAT */}
      <h2 style={{ marginTop: "3rem" }}>Recent Wheat Charts</h2>
      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/inspections/world/export_inspections/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/current_marketing_year_total_commitment/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/gross_new_sales/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/wheat/esr/world/next_marketing_year_outstanding_sales/my`}
            variant="home"
          />
        </div>
      </div>

      <div className="commentary-box">
        <h3>Wheat Commentary:</h3>
        <div dangerouslySetInnerHTML={{ __html: wheatCommentary }} />
      </div>

      {/* SOYBEANS */}
      <h2 style={{ marginTop: "3rem" }}>Recent Soybean Charts</h2>
      <div className="card-grid-2">
        <div className="card">
          <h3>Export Inspections</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/inspections/world/export_inspections/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Total Commitment</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/current_marketing_year_total_commitment/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Gross New Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/gross_new_sales/my`}
            variant="home"
          />
        </div>
        <div className="card">
          <h3>Next Marketing Year Outstanding Sales</h3>
          <ChartViewer
            jsonPath={`${API}/home/soybeans/esr/world/next_marketing_year_outstanding_sales/my`}
            variant="home"
          />
        </div>
      </div>

      <div className="commentary-box">
        <h3>Soybean Commentary:</h3>
        <div dangerouslySetInnerHTML={{ __html: soyCommentary }} />
      </div>

    </div>
  );
}