import { useState, useMemo } from "react";
import ChartViewer from "../components/ChartViewer";

const DATA_SOURCES = ["Inspections", "ESR", "PSD", "Forecasts"];

const BASE_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "Mexico", slug: "mexico" },
  { label: "European Union", slug: "european_union" },
  { label: "China", slug: "china" },
  { label: "Japan", slug: "japan" }
];

const PSD_ONLY_COUNTRY = { label: "United States", slug: "united_states" };

const INSPECTIONS_TYPES = [
  { key: "export_inspections", label: "Export Inspections" }
];

const ESR_TYPES = [
  { key: "weekly_exports", label: "Weekly Exports" },
  { key: "accumulated_exports", label: "Accumulated Exports" },
  { key: "outstanding_sales", label: "Outstanding Sales" },
  { key: "gross_new_sales", label: "Gross New Sales" },
  { key: "current_marketing_year_net_sales", label: "Current MY Net Sales" },
  { key: "current_marketing_year_total_commitment", label: "Current MY Total Commitment" },
  { key: "next_marketing_year_net_sales", label: "Next MY Net Sales" },
  { key: "next_marketing_year_outstanding_sales", label: "Next MY Outstanding Sales" }
];

const PSD_ATTRIBUTES = [
  { key: "area_harvested", label: "Area Harvested" },
  { key: "production", label: "Production" },
  { key: "imports", label: "Imports" },
  { key: "exports", label: "Exports" },
  { key: "ending_stocks", label: "Ending Stocks" }
];

const YEAR_TYPES = [
  { key: "my", label: "Marketing Year" },
  { key: "cal", label: "Calendar Year" }
];

// ⭐ NEW UNIVERSAL JSON PATH BUILDER
function buildJsonPath(dataSource, commodity, countrySlug, dataTypeKey, yearType) {
  const fileSuffix = yearType === "cal" ? "cal" : "my";
  const dataPrefix = dataSource.toLowerCase(); // esr, psd, inspections, forecasts

  // Forecasts → no file exists yet
  if (dataPrefix === "forecasts") return null;

  return `/${dataPrefix}_us_${commodity}_to_${countrySlug}_${dataTypeKey}_last_5_years_${fileSuffix}.json`;
}

export default function Corn() {
  const commodity = "corn";

  const [dataSource, setDataSource] = useState("Inspections");
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState("export_inspections");
  const [yearType, setYearType] = useState("my");

  const countries = useMemo(() => {
    return dataSource === "PSD"
      ? [...BASE_COUNTRIES, PSD_ONLY_COUNTRY]
      : BASE_COUNTRIES;
  }, [dataSource]);

  const dataTypes = useMemo(() => {
    if (dataSource === "Inspections") return INSPECTIONS_TYPES;
    if (dataSource === "ESR") return ESR_TYPES;
    if (dataSource === "PSD") return PSD_ATTRIBUTES;
    if (dataSource === "Forecasts") return []; // no types yet
    return [];
  }, [dataSource]);

  const effectiveDataTypeKey = useMemo(() => {
    const exists = dataTypes.some((t) => t.key === dataTypeKey);
    return exists ? dataTypeKey : dataTypes[0]?.key || "";
  }, [dataTypes, dataTypeKey]);

  const jsonPath = buildJsonPath(
    dataSource,
    commodity,
    countrySlug,
    effectiveDataTypeKey,
    yearType
  );

  function handleDataSourceChange(e) {
    const next = e.target.value;
    setDataSource(next);

    if (next === "Inspections") setDataTypeKey("export_inspections");
    else if (next === "ESR") setDataTypeKey("gross_new_sales");
    else if (next === "PSD") setDataTypeKey(PSD_ATTRIBUTES[0].key);
    else if (next === "Forecasts") setDataTypeKey(""); // no types yet
  }

  return (
    <div className="main-content">
      <h2>Corn</h2>

      <div className="filter-bar-wrapper">
        <div className="filter-bar">

          <div className="filter-item">
            <label>Data Source</label>
            <select value={dataSource} onChange={handleDataSourceChange}>
              {DATA_SOURCES.map((src) => (
                <option key={src} value={src}>{src}</option>
              ))}
            </select>
          </div>

          <div className="filter-item">
            <label>Country</label>
            <select value={countrySlug} onChange={(e) => setCountrySlug(e.target.value)}>
              {countries.map((c) => (
                <option key={c.slug} value={c.slug}>{c.label}</option>
              ))}
            </select>
          </div>

          {dataSource !== "Forecasts" && (
            <div className="filter-item">
              <label>Data Type</label>
              <select
                value={effectiveDataTypeKey}
                onChange={(e) => setDataTypeKey(e.target.value)}
              >
                {dataTypes.map((t) => (
                  <option key={t.key} value={t.key}>{t.label}</option>
                ))}
              </select>
            </div>
          )}

          <div className="filter-item">
            <label>Year Type</label>
            <select value={yearType} onChange={(e) => setYearType(e.target.value)}>
              {YEAR_TYPES.map((y) => (
                <option key={y.key} value={y.key}>{y.label}</option>
              ))}
            </select>
          </div>

        </div>
      </div>

      {/* ⭐ FORECASTS MODE */}
      {dataSource === "Forecasts" && (
        <div className="card card-centered corn-chart">
          <h3>Forecasts – Under Construction</h3>
          <div
            style={{
              height: "700px",
              width: "100%",
              maxWidth: "95%",
              margin: "0 auto",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.2rem",
              color: "#666"
            }}
          >
            Forecasts are under construction.
          </div>
        </div>
      )}

      {/* ⭐ NORMAL CHART MODE */}
      {dataSource !== "Forecasts" && jsonPath && (
        <div className="card card-centered corn-chart">
          <h3>
            {dataSource} – {countries.find((c) => c.slug === countrySlug)?.label} –{" "}
            {dataTypes.find((t) => t.key === effectiveDataTypeKey)?.label} –{" "}
            {YEAR_TYPES.find((y) => y.key === yearType)?.label}
          </h3>

          <div
            style={{
              height: "700px",
              width: "100%",
              maxWidth: "95%",
              margin: "0 auto",
              overflow: "hidden"
            }}
          >
            <ChartViewer jsonPath={jsonPath} variant="corn" />
          </div>
        </div>
      )}
    </div>
  );
}