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
        // Case 1: Full Plotly figure { data, layout }
        if (data.data && data.layout) {
          setFigure({
            data: data.data,
            layout: data.layout,
            config: data.config || {}
          });
          return;
        }

        // Case 2: Array of traces
        if (Array.isArray(data)) {
          setFigure({
            data: data,
            layout: {},
            config: {}
          });
          return;
        }

        // Case 3: Single trace object (your backend case)
        if (!data.data && !data.layout) {
          setFigure({
            data: [data],
            layout: data.layout || {},
            config: data.config || {}
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
    ["corn", "wheat", "soybeans", "soybean_oil", "soybean_meal"].includes(
      variant
    );

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