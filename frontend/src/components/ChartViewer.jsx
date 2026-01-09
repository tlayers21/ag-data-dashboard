import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function ChartViewer({ jsonPath }) {
  const [figure, setFigure] = useState(null);

  useEffect(() => {
    fetch(jsonPath)
      .then((res) => res.json())
      .then((data) => setFigure(data))
      .catch((err) => console.error("Error loading chart JSON:", err));
  }, [jsonPath]);

  if (!figure) {
    return (
      <div style={{ height: "200px", display: "flex", alignItems: "center", justifyContent: "center", color: "#777" }}>
        Loading chart…
      </div>
    );
  }

  return (
    <Plot
      data={figure.data}
      layout={figure.layout}
      config={figure.config || {}}
      style={{ width: "100%", height: "100%" }}
      useResizeHandler={true}
    />
  );
}