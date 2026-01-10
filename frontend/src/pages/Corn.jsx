import { useState, useMemo } from "react";
import ChartViewer from "../components/ChartViewer";

const DATA_SOURCES = ["Inspections", "ESR", "PSD"];

const BASE_COUNTRIES = [
  { label: "World", slug: "world" },
  { label: "Mexico", slug: "mexico" },
  { label: "European Union", slug: "european_union" },
  { label: "China", slug: "china" },
  { label: "Japan", slug: "japan" }
];

const PSD_ONLY_COUNTRY = { label: "United States", slug: "united_states" };

const INSPECTIONS_TYPES = [
  { key: "inspections", label: "Export Inspections" }
];

const ESR_TYPES = [
  { key: "weekly_exports", label: "Weekly Exports" },
  { key: "accumulated_exports", label: "Accumulated Exports" },
  { key: "outstanding_sales", label: "Outstanding Sales" },
  { key: "gross_new_sales", label: "Gross New Sales" },
  { key: "current_marketing_year_net_sales", label: "Current Marketing Year Net Sales" },
  { key: "current_marketing_year_total_commitment", label: "Current Marketing Year Total Commitment" },
  { key: "next_marketing_year_outstanding_sales", label: "Next Marketing Year Outstanding Sales" },
  { key: "next_marketing_year_net_sales", label: "Next Marketing Year Net Sales" }
];

const PSD_ATTRIBUTES = [
  { key: "area_harvested", label: "Area Harvested" },
  { key: "crush", label: "Crush" },
  { key: "beginning_stocks", label: "Beginning Stocks" },
  { key: "production", label: "Production" },
  { key: "imports", label: "Imports" },
  { key: "trade_year_imports", label: "Trade Year Imports" },
  { key: "trade_year_imports_from_us", label: "Trade Year Imports from U.S." },
  { key: "total_supply", label: "Total Supply" },
  { key: "exports", label: "Exports" },
  { key: "trade_year_exports", label: "Trade Year Exports" },
  { key: "domestic_consumption", label: "Domestic Consumption" },
  { key: "feed_domestic_consumption", label: "Feed Domestic Consumption" },
  { key: "industrial_domestic_consumption", label: "Industrial Domestic Consumption" },
  { key: "food_use_domestic_consumption", label: "Food Use Domestic Consumption" },
  { key: "feed_waste_domestic_consumption", label: "Feed Waste Domestic Consumption" },
  { key: "ending_stocks", label: "Ending Stocks" },
  { key: "total_distribution", label: "Total Distribution" },
  { key: "extraction_rate", label: "Extraction Rate" },
  { key: "yield", label: "Yield" },
  { key: "food_seed_industrial_consumption", label: "Food, Seed, and Industrial Consumption" },
  { key: "soybean_meal_equivalent", label: "Soybean Meal Equivalent" }
];

function buildJsonPath(dataSource, countrySlug, dataTypeKey) {
  if (!dataSource || !countrySlug || !dataTypeKey) return "";

  if (dataSource === "Inspections" || dataSource === "ESR") {
    return `/us_corn_to_${countrySlug}_${dataTypeKey}_last_5_years_my.json`;
  }

  if (dataSource === "PSD") {
    return `/us_corn_psd_${countrySlug}_${dataTypeKey}.json`;
  }

  return "";
}

export default function Corn() {
  const [dataSource, setDataSource] = useState("Inspections");
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState("inspections");

  const countries = useMemo(() => {
    return dataSource === "PSD"
      ? [...BASE_COUNTRIES, PSD_ONLY_COUNTRY]
      : BASE_COUNTRIES;
  }, [dataSource]);

  const dataTypes = useMemo(() => {
    if (dataSource === "Inspections") return INSPECTIONS_TYPES;
    if (dataSource === "ESR") return ESR_TYPES;
    if (dataSource === "PSD") return PSD_ATTRIBUTES;
    return [];
  }, [dataSource]);

  const effectiveDataTypeKey = useMemo(() => {
    const exists = dataTypes.some((t) => t.key === dataTypeKey);
    return exists ? dataTypeKey : dataTypes[0]?.key || "";
  }, [dataTypes, dataTypeKey]);

  const jsonPath = buildJsonPath(dataSource, countrySlug, effectiveDataTypeKey);

  function handleDataSourceChange(e) {
    const nextSource = e.target.value;
    setDataSource(nextSource);

    if (nextSource === "Inspections") setDataTypeKey("inspections");
    else if (nextSource === "ESR") setDataTypeKey("gross_new_sales");
    else if (nextSource === "PSD") setDataTypeKey(PSD_ATTRIBUTES[0].key);
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
            <select
              value={countrySlug}
              onChange={(e) => setCountrySlug(e.target.value)}
            >
              {countries.map((c) => (
                <option key={c.slug} value={c.slug}>{c.label}</option>
              ))}
            </select>
          </div>

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
        </div>
      </div>

      {jsonPath && (
        <div className="card card-centered corn-chart">
          <h3>
            {dataSource} – {countries.find((c) => c.slug === countrySlug)?.label} –{" "}
            {dataTypes.find((t) => t.key === effectiveDataTypeKey)?.label}
          </h3>

          <div style={{
                 height: "700px",
                 width: "100%",
                 maxwidth: "95%",
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