import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

// variant = "home" or "corn"
export default function ChartViewer({ jsonPath, variant = "home" }) {
  const [figure, setFigure] = useState(null);

  useEffect(() => {
    fetch(jsonPath)
      .then((res) => res.json())
      .then((data) => {
        const fig = data.figure || data;
        setFigure(fig);
      })
      .catch((err) => console.error("Error loading chart JSON:", err));
  }, [jsonPath]);

  if (!figure) {
    return (
      <div
        style={{
          height: "200px",
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

  if (variant === "corn") {
    layout = {
      ...layout,
      legend: {
        ...(layout.legend || {}),
        orientation: "h",
        y: -0.2,
        x: 0.5,
        xanchor: "center"
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