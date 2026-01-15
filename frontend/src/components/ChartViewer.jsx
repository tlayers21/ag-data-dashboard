import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function ChartViewer({ jsonPath, variant = "home" }) {
  const [figure, setFigure] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
    setFigure(null);

    fetch(jsonPath)
      .then(async (res) => {
        if (!res.ok) throw new Error("Bad response");

        // Try to parse JSON safely
        const text = await res.text();
        try {
          return JSON.parse(text);
        } catch {
          throw new Error("Invalid JSON");
        }
      })
      .then((data) => {
        if (!data || data.error) {
          setError(true);
          return;
        }

        // Full Plotly figure
        if (data.data && data.layout) {
          setFigure({
            data: data.data,
            layout: data.layout,
            config: data.config || {}
          });
          return;
        }

        // Array of traces
        if (Array.isArray(data)) {
          setFigure({
            data: data,
            layout: {},
            config: {}
          });
          return;
        }

        // Single trace object
        if (typeof data === "object" && !data.data && !data.layout) {
          setFigure({
            data: [data],
            layout: {},
            config: {}
          });
          return;
        }

        // Fallback
        setFigure(data);
      })
      .catch(() => setError(true));
  }, [jsonPath]);

  const isCommodityPage =
    variant !== "home" &&
    ["corn", "wheat", "soybeans", "soybean-oil", "soybean-meal"].includes(
      variant
    );

  // Commodity page error message
  if (error && isCommodityPage) {
    return (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1.1rem",
          color: "#666",
          textAlign: "center",
          padding: "1rem"
        }}
      >
        Data for this selection is not available.
      </div>
    );
  }

  // Home page error message
  if (error && !isCommodityPage) {
    return (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1rem",
          color: "#999"
        }}
      >
        Chart unavailable.
      </div>
    );
  }

  // Loading
  if (!figure) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#777"
        }}
      >
        Loading chart…
      </div>
    );
  }

  // Layout adjustments
  let layout = { ...figure.layout };

  if (isCommodityPage) {
    layout = {
      ...layout,
      legend: {
        ...(layout.legend || {}),
        orientation: "h",
        y: -0.2,
        x: 0.5,
        xanchor: "center"
      },
      margin: {
        ...(layout.margin || {}),
        b: 120
      }
    };
  }

  return (
    <Plot
      data={figure.data}
      layout={layout}
      config={figure.config || {}}
      style={{ width: "100%", height: "100%" }}
      useResizeHandler={true}
    />
  );
}