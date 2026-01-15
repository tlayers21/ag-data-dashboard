import { useEffect, useState, useRef } from "react";
import ChartViewer from "../components/ChartViewer";
import { loadCommentary } from "../utils/loadCommentary";

export default function Home() {
  const firstLoadRef = useRef(true);

  const [loading, setLoading] = useState(true);

  const [loadingMessage, setLoadingMessage] = useState("Warming up the data engine…");

  const [cornCommentary, setCornCommentary] = useState("");
  const [wheatCommentary, setWheatCommentary] = useState("");
  const [soyCommentary, setSoyCommentary] = useState("");

  const API = process.env.REACT_APP_API_BASE;

  const messages = [
    "Warming up the data engine…",
    "Retrieving export sales report metrics…",
    "Loading production, supply and distribution numbers…",
    "Parsing the latest inspections data…",
    "Processing and transforming raw datasets…",
    "Merging multi‑commodity analytics…",
    "Generating charts and commentary…",
    "Almost ready. Charts may take 1-2 minutes to fully render…"
  ];

  useEffect(() => {
  let messageIndex = 0;

  const interval = setInterval(() => {
    messageIndex++;

    if (messageIndex >= messages.length - 1) {
      setLoadingMessage(messages[messages.length - 1]);
      clearInterval(interval);
      return;
    }

    setLoadingMessage(messages[messageIndex]);
  }, 3750);

  return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    async function load() {
      if (!firstLoadRef.current) {
        setLoading(false);
        return;
      }

      firstLoadRef.current = false;

      document.documentElement.style.setProperty("--loading-duration", "30s");

      try {
        const { corn, wheat, soybeans } = await loadCommentary();
        setCornCommentary(corn);
        setWheatCommentary(wheat);
        setSoyCommentary(soybeans);
      } catch (err) {
        console.error("Commentary failed:", err);
      }

      setTimeout(() => {
        setLoading(false);
      }, 24000);
    }

    load();
  }, []);

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="loading-title">Loading Dashboard</div>

        <div className="progress-container">
          <div className="progress-bar"></div>
        </div>

        <p className="loading-message">{loadingMessage}</p>
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