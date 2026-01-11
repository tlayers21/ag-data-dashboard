import { useState, useMemo, useEffect } from "react";
import ChartViewer from "../components/ChartViewer";

// -----------------------------
// DATA SOURCE OPTIONS
// -----------------------------
const DATA_SOURCES = ["Inspections", "ESR", "PSD", "Forecasts"];

// -----------------------------
// COUNTRY OPTIONS
// -----------------------------
const BASE_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "Mexico", slug: "mexico" },
  { label: "European Union", slug: "european_union" },
  { label: "China", slug: "china" },
  { label: "Japan", slug: "japan" }
];

const PSD_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "United States", slug: "united_states" },
  { label: "Mexico", slug: "mexico" },
  { label: "European Union", slug: "european_union" },
  { label: "China", slug: "china" },
  { label: "Japan", slug: "japan" }
];

// -----------------------------
// INSPECTIONS TYPES
// -----------------------------
const INSPECTIONS_TYPES = [
  { key: "export_inspections", label: "Export Inspections" }
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
// PSD ATTRIBUTES
// -----------------------------
const PSD_ATTRIBUTES = [
  { key: "area_harvested", label: "Area Harvested" },
  { key: "beginning_stocks", label: "Beginning Stocks" },
  { key: "production", label: "Production" },
  { key: "imports", label: "Imports" },
  { key: "trade_year_imports", label: "Trade Year Imports" },
  { key: "trade_year_imports_from_united_states", label: "Trade Year Imports From U.S." },
  { key: "total_supply", label: "Total Supply" },
  { key: "exports", label: "Exports" },
  { key: "trade_year_exports", label: "Trade Year Exports" },
  { key: "domestic_consumption", label: "Domestic Consumption" },
  { key: "feed_domestic_consumption", label: "Feed Domestic Consumption" },
  { key: "ending_stocks", label: "Ending Stocks" },
  { key: "total_distribution", label: "Total Distribution" },
  { key: "yield", label: "Yield" }
];

// -----------------------------
// YEAR TYPE OPTIONS
// -----------------------------
const YEAR_TYPES = [
  { key: "my", label: "Marketing Year" },
  { key: "cal", label: "Calendar Year" }
];

// -----------------------------
// UNIVERSAL JSON PATH BUILDER
// -----------------------------
function buildJsonPath(dataSource, commodity, countrySlug, dataTypeKey, yearType) {
  const fileSuffix = yearType === "cal" ? "cal" : "my";
  const dataPrefix = dataSource.toLowerCase();

  if (dataPrefix === "forecasts") return null;

  if (dataPrefix === "psd") {
    return `/${dataPrefix}_${commodity}_for_${countrySlug}_${dataTypeKey}_last_5_years_${fileSuffix}.json`;
  }

  return `/${dataPrefix}_us_${commodity}_to_${countrySlug}_${dataTypeKey}_last_5_years_${fileSuffix}.json`;
}

// -----------------------------
// MAIN COMPONENT
// -----------------------------
export default function Corn() {
  const commodity = "corn";

  const [dataSource, setDataSource] = useState("Inspections");
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState("export_inspections");
  const [yearType, setYearType] = useState("my");

  // Force Marketing Year when PSD is selected
  useEffect(() => {
    if (dataSource === "PSD" && yearType === "cal") {
      setYearType("my");
    }
  }, [dataSource, yearType]);

  // Country list logic
  const countries = useMemo(() => {
    if (dataSource === "Inspections") {
      return [{ label: "World", slug: "world" }];
    }
    return dataSource === "PSD" ? PSD_COUNTRIES : BASE_COUNTRIES;
  }, [dataSource]);

  // Data type list logic
  const dataTypes = useMemo(() => {
    if (dataSource === "Inspections") return INSPECTIONS_TYPES;
    if (dataSource === "ESR") return ESR_TYPES;

    if (dataSource === "PSD") {
      if (countrySlug === "united_states") {
        return PSD_ATTRIBUTES.filter(
          (attr) => attr.key !== "trade_year_imports_from_united_states"
        );
      }
      return PSD_ATTRIBUTES;
    }

    return [];
  }, [dataSource, countrySlug]);

  // Ensure valid data type
  const effectiveDataTypeKey = useMemo(() => {
    const exists = dataTypes.some((t) => t.key === dataTypeKey);
    return exists ? dataTypeKey : dataTypes[0]?.key || "";
  }, [dataTypes, dataTypeKey]);

  // Build JSON path
  const jsonPath = buildJsonPath(
    dataSource,
    commodity,
    countrySlug,
    effectiveDataTypeKey,
    yearType
  );

  // Handle data source switching
  function handleDataSourceChange(e) {
    const next = e.target.value;
    setDataSource(next);

    if (next === "Inspections") {
      setCountrySlug("world");
      setDataTypeKey("export_inspections");
    } else if (next === "ESR") {
      setDataTypeKey(ESR_TYPES[0].key);
    } else if (next === "PSD") {
      setDataTypeKey(PSD_ATTRIBUTES[0].key);
    } else if (next === "Forecasts") {
      setDataTypeKey("");
    }
  }

  return (
    <div className="main-content">
      <h2>Corn</h2>

      {/* FILTER BAR */}
      <div className="filter-bar-wrapper">
        <div className="filter-bar">

          {/* Data Source */}
          <div className="filter-item">
            <label>Data Source</label>
            <select value={dataSource} onChange={handleDataSourceChange}>
              {DATA_SOURCES.map((src) => (
                <option key={src} value={src}>{src}</option>
              ))}
            </select>
          </div>

          {/* Country */}
          <div className="filter-item">
            <label>Country</label>
            <select
              value={countrySlug}
              onChange={(e) => setCountrySlug(e.target.value)}
            >
              {countries.map((c) => (
                <option key={c.slug} value={c.slug}>{c.label}</option>
              ))}
            </select>
          </div>

          {/* Data Type */}
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

          {/* Year Type */}
          <div className="filter-item">
            <label>Year Type</label>
            <select
              value={yearType}
              onChange={(e) => setYearType(e.target.value)}
            >
              {YEAR_TYPES
                .filter((y) => !(dataSource === "PSD" && y.key === "cal"))
                .map((y) => (
                  <option key={y.key} value={y.key}>{y.label}</option>
                ))}
            </select>
          </div>

        </div>
      </div>

      {/* FORECASTS MODE */}
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

      {/* NORMAL CHART MODE */}
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