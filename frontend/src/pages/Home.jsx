import { Fragment, useEffect, useState } from "react";
import ChartViewer from "../components/ChartViewer";
import { loadCommentary } from "../utils/loadCommentary";

const API = process.env.REACT_APP_API_BASE;

const LOADING_MESSAGES = [
  "Warming up the data engine…",
  "Retrieving export sales report metrics…",
  "Loading production, supply and distribution numbers…",
  "Parsing the latest inspections data…",
  "Processing and transforming raw datasets…",
  "Generating charts and commentary…",
  "Almost ready. Charts may take 1-2 minutes to fully load…"
];

const SECTIONS = [
  { slug: "corn", title: "Recent Corn Charts", commentaryTitle: "Corn Commentary:" },
  { slug: "wheat", title: "Recent Wheat Charts", commentaryTitle: "Wheat Commentary:" },
  { slug: "soybeans", title: "Recent Soybean Charts", commentaryTitle: "Soybean Commentary:" }
];

const CHARTS = [
  { title: "Export Inspections", path: "inspections/world/export_inspections/my" },
  { title: "Total Commitment", path: "esr/world/current_marketing_year_total_commitment/my" },
  { title: "Gross New Sales", path: "esr/world/gross_new_sales/my" },
  { title: "Next Marketing Year Outstanding Sales", path: "esr/world/next_marketing_year_outstanding_sales/my" }
];

export default function Home() {
  // Only show the loading screen on the first visit of the session
  const [loading, setLoading] = useState(() => sessionStorage.getItem("homeLoaded") !== "true");
  const [messageIndex, setMessageIndex] = useState(0);
  const [commentary, setCommentary] = useState(null);

  useEffect(() => {
    if (!loading) return;
    sessionStorage.setItem("homeLoaded", "true");

    const interval = setInterval(() => {
      setMessageIndex((i) => Math.min(i + 1, LOADING_MESSAGES.length - 1));
    }, 2000);
    const timeout = setTimeout(() => setLoading(false), 10900);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [loading]);

  useEffect(() => {
    loadCommentary().then(setCommentary);
  }, []);

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="loading-title">Loading Dashboard</div>

        <div className="progress-container">
          <div className="progress-bar"></div>
        </div>

        <p className="loading-message">{LOADING_MESSAGES[messageIndex]}</p>
      </div>
    );
  }

  return (
    <div className="main-content">
      {SECTIONS.map((section, i) => (
        <Fragment key={section.slug}>
          <h2 style={i > 0 ? { marginTop: "3rem" } : undefined}>{section.title}</h2>
          <div className="card-grid-2">
            {CHARTS.map((chart) => (
              <div className="card" key={chart.path}>
                <h3>{chart.title}</h3>
                <ChartViewer jsonPath={`${API}/home/${section.slug}/${chart.path}`} variant="home" />
              </div>
            ))}
          </div>

          <div className="commentary-box">
            <h3>{section.commentaryTitle}</h3>
            {commentary === null ? (
              <p className="commentary-loading">Loading commentary…</p>
            ) : (
              <div dangerouslySetInnerHTML={{ __html: commentary[section.slug] }} />
            )}
          </div>
        </Fragment>
      ))}
    </div>
  );
}
