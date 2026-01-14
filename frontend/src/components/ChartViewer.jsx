import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function ChartViewer({ jsonPath, variant = "home" }) {
  const [figure, setFigure] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
    setFigure(null);

    fetch(jsonPath)
      .then((res) => {
        if (!res.ok) throw new Error("API returned error");
        return res.json();
      })
      .then((data) => {
        if (data.error) {
          setError(true);
          return;
        }

        let fig = data;

        // Full Plotly figure { data, layout }
        if (fig.data && fig.layout) {
          setFigure({
            data: fig.data,
            layout: fig.layout,
            config: fig.config || {}
          });
          return;
        }

        // Array of traces
        if (Array.isArray(fig)) {
          setFigure({
            data: fig,
            layout: {},
            config: {}
          });
          return;
        }

        // Single trace object (backend case)
        if (!fig.data && !fig.layout) {
          setFigure({
            data: [fig],
            layout: {},
            config: {}
          });
          return;
        }

        // Fallback
        setFigure(fig);
      })
      .catch(() => setError(true));
  }, [jsonPath]);

  const isCommodityPage =
    variant !== "home" &&
    ["corn", "wheat", "soybeans", "soybean_oil", "soybean_meal"].includes(
      variant
    );

  // Error message for commodity pages
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

  // Loading state
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

  // Apply commodity-specific layout adjustments
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