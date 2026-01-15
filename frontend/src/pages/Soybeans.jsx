import { useState, useMemo, useEffect } from "react";
import ChartViewer from "../components/ChartViewer";
import Dropdown from "../components/Dropdown";

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
  { label: "European Union", slug: "european-union" },
  { label: "China", slug: "china" },
  { label: "Japan", slug: "japan" }
];

const PSD_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "United States", slug: "united-states" },
  { label: "Mexico", slug: "mexico" },
  { label: "European Union", slug: "european-union" },
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
  { key: "crush", label: "Crush" },
  { key: "beginning_stocks", label: "Beginning Stocks" },
  { key: "production", label: "Production" },
  { key: "imports", label: "Imports" },
  { key: "total_supply", label: "Total Supply" },
  { key: "exports", label: "Exports" },
  { key: "domestic_consumption", label: "Domestic Consumption" },
  { key: "food_use_domestic_consumption", label: "Food Use Domestic Consumption" },
  { key: "feed_waste_domestic_consumption", label: "Feed Waste Domestic Consumption" },
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
// API URL BUILDER
// -----------------------------
const API_BASE = process.env.REACT_APP_API_BASE;

function buildApiUrl(dataSource, commodity, countrySlug, dataTypeKey, yearType) {
  const ds = dataSource.toLowerCase();
  if (ds === "forecasts") return null;

  return `${API_BASE}/${commodity}/${ds}/${countrySlug}/${dataTypeKey}/${yearType}`;
}

// -----------------------------
// MAIN COMPONENT
// -----------------------------
export default function Soybeans() {
  const commodity = "soybeans";

  const [dataSource, setDataSource] = useState("Inspections");
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState("export_inspections");
  const [yearType, setYearType] = useState("my");

  // PSD: force Marketing Year
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
      if (countrySlug === "united-states") {
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

  // Build API URL
  const jsonPath = buildApiUrl(
    dataSource,
    commodity,
    countrySlug,
    effectiveDataTypeKey,
    yearType
  );

  // Handle data source switching
  function handleDataSourceChange(value) {
    setDataSource(value);

    if (value === "Inspections") {
      setCountrySlug("world");
      setDataTypeKey("export_inspections");
    } else if (value === "ESR") {
      setDataTypeKey(ESR_TYPES[0].key);
    } else if (value === "PSD") {
      setDataTypeKey(PSD_ATTRIBUTES[0].key);
    } else if (value === "Forecasts") {
      setDataTypeKey("");
    }
  }

  return (
    <div className="main-content">
      <h2>Soybeans</h2>

      {/* FILTER BAR */}
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
              items={YEAR_TYPES.filter(
                (y) => !(dataSource === "PSD" && y.key === "cal")
              ).map((y) => ({
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
        <div className="card card-centered soybeans-chart">
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
        <div className="card card-centered soybeans-chart">
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
            <ChartViewer jsonPath={jsonPath} variant="soybeans" />
          </div>
        </div>
      )}
    </div>
  );
}