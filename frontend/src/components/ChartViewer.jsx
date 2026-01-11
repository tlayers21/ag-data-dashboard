import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

// variant = "home" or any commodity: "corn", "wheat", "soybeans", "soybean_oil", "soybean_meal"
export default function ChartViewer({ jsonPath, variant = "home" }) {
  const [figure, setFigure] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
    setFigure(null);

    fetch(jsonPath)
      .then((res) => {
        if (!res.ok) {
          throw new Error("File not found");
        }
        return res.json();
      })
      .then((data) => {
        const fig = data.figure || data;
        setFigure(fig);
      })
      .catch(() => {
        setError(true);
      });
  }, [jsonPath]);

  // -----------------------------
  // ERROR STATE (commodity pages)
  // -----------------------------
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

  // -----------------------------
  // LOADING STATE
  // -----------------------------
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

  // -----------------------------
  // LEGEND LOGIC (all commodities)
  // -----------------------------
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
        b: 120 // ensures space for horizontal legend
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