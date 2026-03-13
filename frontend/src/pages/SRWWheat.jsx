import { useState, useMemo } from "react";
import ChartViewer from "../components/ChartViewer";
import Dropdown from "../components/Dropdown";

// -----------------------------
// DATA SOURCE OPTIONS
// -----------------------------
const DATA_SOURCES = ["ESR", "Forecasts"];

// -----------------------------
// COUNTRY OPTIONS
// -----------------------------
const BASE_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "Mexico", slug: "mexico" },
  { label: "Japan", slug: "japan" },
  { label: "South Korea", slug: "south-korea" },
  { label: "Colombia", slug: "colombia" },
  { label: "European Union", slug: "european-union" },
  { label: "Taiwan", slug: "taiwan" },
  { label: "Guatemala", slug: "guatemala" },
  { label: "Vietnam", slug: "vietnam" },
  { label: "Canada", slug: "canada" },
  { label: "Honduras", slug: "honduras" },
  { label: "Philippines", slug: "philippines" },
  { label: "Nigeria", slug: "nigeria" },
  { label: "Indonesia", slug: "indonesia" },
  { label: "Thailand", slug: "thailand" },
  { label: "China", slug: "china" },
  { label: "Egypt", slug: "egypt" },
  { label: "Pakistan", slug: "pakistan" },
  { label: "Bangladesh", slug: "bangladesh" }
];

// -----------------------------
// ESR TYPES
// -----------------------------
const ESR_TYPES = [
  { key: "weekly_exports", label: "Weekly Exports" },
  { key: "accumulated_exports", label: "Accumulated Exports" },
  { key: "outstanding_sales", label: "Outstanding Sales" },
  { key: "gross_new_sales", label: "Gross New Sales" },
  { key: "current_marketing_year_net_sales", label: "Current Marketing Year Net Sales" },
  { key: "current_marketing_year_total_commitment", label: "Current Marketing Year Total Commitment" },
  { key: "next_marketing_year_net_sales", label: "Next Marketing Year Net Sales" },
  { key: "next_marketing_year_outstanding_sales", label: "Next Marketing Year Outstanding Sales" }
];

// -----------------------------
// YEAR TYPE OPTIONS
// -----------------------------
const YEAR_TYPES = [
  { key: "my", label: "Marketing Year" },
  { key: "cal", label: "Calendar Year" }
];

// -----------------------------
// API URL BUILDER
// -----------------------------
function buildApiUrl(dataSource, commodity, countrySlug, dataTypeKey, yearType) {
  const ds = dataSource.toLowerCase();
  if (ds === "forecasts") return null;

  return `${process.env.REACT_APP_API_BASE}/${commodity}/${ds}/${countrySlug}/${dataTypeKey}/${yearType}`;
}

// -----------------------------
// MAIN COMPONENT
// -----------------------------
export default function SRWWheat() {
  const commodity = "srw-wheat";

  const [dataSource, setDataSource] = useState("ESR");
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState(ESR_TYPES[0].key);
  const [yearType, setYearType] = useState("my");

  const countries = useMemo(() => {
    return BASE_COUNTRIES;
  }, []);

  const dataTypes = useMemo(() => {
    if (dataSource === "ESR") return ESR_TYPES;
    return [];
  }, [dataSource]);

  const effectiveDataTypeKey = useMemo(() => {
    const exists = dataTypes.some((t) => t.key === dataTypeKey);
    return exists ? dataTypeKey : dataTypes[0]?.key || "";
  }, [dataTypes, dataTypeKey]);

  const jsonPath = buildApiUrl(
    dataSource,
    commodity,
    countrySlug,
    effectiveDataTypeKey,
    yearType
  );

  function handleDataSourceChange(value) {
    setDataSource(value);

    if (value === "ESR") {
      setDataTypeKey(ESR_TYPES[0].key);
    } else if (value === "Forecasts") {
      setDataTypeKey("");
    }
  }

  return (
    <div className="main-content">
      <h2>SRW Wheat</h2>

      <div className="filter-bar-wrapper">
        <div className="filter-bar">

          {/* Data Source */}
          <div className="filter-item">
            <label>Data Source</label>
            <Dropdown
              label={dataSource}
              className="filter-dropdown"
              items={DATA_SOURCES.map((src) => ({
                label: src,
                value: src
              }))}
              onSelect={(value) => handleDataSourceChange(value)}
            />
          </div>

          {/* Country */}
          <div className="filter-item">
            <label>Country</label>
            <Dropdown
              label={countries.find((c) => c.slug === countrySlug)?.label}
              className="filter-dropdown"
              items={countries.map((c) => ({
                label: c.label,
                value: c.slug
              }))}
              onSelect={(value) => setCountrySlug(value)}
            />
          </div>

          {/* Data Type */}
          {dataSource !== "Forecasts" && (
            <div className="filter-item">
              <label>Data Type</label>
              <Dropdown
                label={
                  dataTypes.find((t) => t.key === effectiveDataTypeKey)?.label
                }
                className="filter-dropdown"
                items={dataTypes.map((t) => ({
                  label: t.label,
                  value: t.key
                }))}
                onSelect={(value) => setDataTypeKey(value)}
              />
            </div>
          )}

          {/* Year Type */}
          <div className="filter-item">
            <label>Year Type</label>
            <Dropdown
              label={YEAR_TYPES.find((y) => y.key === yearType)?.label}
              className="filter-dropdown"
              items={YEAR_TYPES.map((y) => ({
                label: y.label,
                value: y.key
              }))}
              onSelect={(value) => setYearType(value)}
            />
          </div>

        </div>
      </div>

      {/* FORECASTS MODE */}
      {dataSource === "Forecasts" && (
        <div className="card card-centered srw-wheat-chart">
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

      {/* NORMAL CHART MODE */}
      {dataSource !== "Forecasts" && jsonPath && (
        <div className="card card-centered srw-wheat-chart">
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
            <ChartViewer jsonPath={jsonPath} variant="srw-wheat" />
          </div>
        </div>
      )}
    </div>
  );
}