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

        const raw = await res.text();
        try {
          return JSON.parse(raw);
        } catch {
          throw new Error("Invalid JSON");
        }
      })
      .then((data) => {
        if (!data || data.error) {
          setError(true);
          return;
        }

        if (data.data && data.layout) {
          setFigure({
            data: data.data,
            layout: data.layout,
            config: data.config || {}
          });
          return;
        }

        if (Array.isArray(data)) {
          setFigure({
            data: data,
            layout: {},
            config: {}
          });
          return;
        }

        if (typeof data === "object" && !data.data && !data.layout) {
          setFigure({
            data: [data],
            layout: {},
            config: {}
          });
          return;
        }

        setFigure(data);
      })
      .catch(() => setError(true));
  }, [jsonPath, variant]);

  const isCommodityPage =
    variant !== "home" &&
    ["corn", "wheat", "soybeans", "soybean-oil", "soybean-meal"].includes(
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

  if (variant === "home") {
    layout = {
      ...layout,
      legend: {
        ...(layout.legend || {}),
        orientation: "h",
        y: -0.34,
        yanchor: "top",
        x: 0.5,
        xanchor: "center"
      },
      margin: {
        ...(layout.margin || {}),
        b: 140,
        t: 60,
        l: 60,
        r: 40
      },
      xaxis: {
        ...(layout.xaxis || {}),
        tickangle: -45,
        automargin: true
      }
    };
  }

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
      },
      xaxis: {
        ...(layout.xaxis || {}),
        tickangle: -45,
        automargin: true
      }
    };
  }

  const chartHeight = isCommodityPage ? "520px" : "480px";

  return (
    <div className={variant === "home" ? "home-chart" : ""}>
      <Plot
        data={figure.data}
        layout={layout}
        config={figure.config || {}}
        style={{ width: "100%", height: chartHeight }}
        useResizeHandler={true}
      />
    </div>
  );
}