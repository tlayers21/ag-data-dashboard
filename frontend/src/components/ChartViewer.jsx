import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

// x-axis title spacing differs between Safari and Chromium
const STANDOFF = isSafari
  ? { home: 14, commodity: 16 }
  : { home: 40, commodity: 70 };

export default function ChartViewer({ jsonPath, variant = "home" }) {
  const [figure, setFigure] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    // Ignore responses for a previous selection that arrive after a newer one
    let stale = false;
    setError(false);
    setFigure(null);

    fetch(jsonPath)
      .then((res) => {
        if (!res.ok) throw new Error("Bad response");
        return res.json();
      })
      .then((data) => {
        if (stale) return;
        if (!data || data.error) {
          setError(true);
        } else if (data.data) {
          setFigure({ data: data.data, layout: data.layout || {}, config: data.config || {} });
        } else {
          // A bare trace or list of traces
          setFigure({ data: [data].flat(), layout: {}, config: {} });
        }
      })
      .catch(() => !stale && setError(true));

    return () => {
      stale = true;
    };
  }, [jsonPath]);

  const isHome = variant === "home";

  if (error) {
    return (
      <div className="chart-message">
        {isHome ? "Chart unavailable." : "Data for this selection is not available."}
      </div>
    );
  }

  if (!figure) {
    return <div className="chart-message">Loading chart…</div>;
  }

  const { layout } = figure;
  const xaxis = {
    ...layout.xaxis,
    tickangle: -45,
    automargin: true,
    title: { ...layout.xaxis?.title, standoff: isHome ? STANDOFF.home : STANDOFF.commodity }
  };

  const adjustedLayout = isHome
    ? {
        ...layout,
        title: { ...layout.title, font: { ...layout.title?.font, size: 14 } },
        legend: { ...layout.legend, orientation: "h", y: -0.34, yanchor: "top", x: 0.5, xanchor: "center" },
        margin: { ...layout.margin, b: 140, t: 60, l: 60, r: 40 },
        xaxis
      }
    : {
        ...layout,
        legend: { ...layout.legend, orientation: "h", y: -0.2, x: 0.5, xanchor: "center" },
        margin: { ...layout.margin, b: 120 },
        xaxis
      };

  return (
    <Plot
      // Force SVG rendering by swapping WebGL traces for regular ones
      data={figure.data.map((trace) => ({
        ...trace,
        type: trace.type === "scattergl" ? "scatter" : trace.type
      }))}
      layout={adjustedLayout}
      config={{ ...figure.config, renderMode: "svg", displayModeBar: false, responsive: true }}
      style={{ width: "100%", height: isHome ? "480px" : "520px" }}
      useResizeHandler
    />
  );
}
