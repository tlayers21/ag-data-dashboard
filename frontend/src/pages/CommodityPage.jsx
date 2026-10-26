import { useState } from "react";
import ChartViewer from "../components/ChartViewer";
import Dropdown from "../components/Dropdown";
import {
  INSPECTIONS_TYPES,
  ESR_TYPES,
  YEAR_TYPES,
  BASE_COUNTRIES,
  PSD_COUNTRIES
} from "../commodities";

const WORLD_ONLY = [BASE_COUNTRIES[0]];

export default function CommodityPage({ slug, name, dataSources, psdAttributes = [] }) {
  const typesFor = (source) =>
    ({ Inspections: INSPECTIONS_TYPES, ESR: ESR_TYPES, PSD: psdAttributes })[source] || [];

  const [dataSource, setDataSource] = useState(dataSources[0]);
  const [countrySlug, setCountrySlug] = useState("world");
  const [dataTypeKey, setDataTypeKey] = useState(typesFor(dataSources[0])[0].key);
  const [yearType, setYearType] = useState("my");

  const countriesFor = (source) =>
    source === "Inspections" ? WORLD_ONLY : source === "PSD" ? PSD_COUNTRIES : BASE_COUNTRIES;
  const countries = countriesFor(dataSource);

  // The U.S. can't import from itself
  const dataTypes = typesFor(dataSource).filter(
    (t) => !(countrySlug === "united-states" && t.key === "trade_year_imports_from_united_states")
  );

  // Fall back to the first data type if the selected one isn't offered here
  const effectiveDataTypeKey = dataTypes.some((t) => t.key === dataTypeKey)
    ? dataTypeKey
    : dataTypes[0]?.key || "";

  // PSD is only published by marketing year
  const yearTypes = YEAR_TYPES.filter((y) => !(dataSource === "PSD" && y.key === "cal"));

  const countryLabel = countries.find((c) => c.slug === countrySlug)?.label;
  const dataTypeLabel = dataTypes.find((t) => t.key === effectiveDataTypeKey)?.label;
  const yearLabel = YEAR_TYPES.find((y) => y.key === yearType)?.label;

  function handleDataSourceChange(next) {
    setDataSource(next);
    setDataTypeKey(typesFor(next)[0]?.key || "");
    // e.g. United States is only offered under PSD
    if (!countriesFor(next).some((c) => c.slug === countrySlug)) setCountrySlug("world");
    if (next === "PSD") setYearType("my");
  }

  const filters = [
    {
      label: "Data Source",
      value: dataSource,
      items: dataSources.map((src) => ({ label: src, value: src })),
      onSelect: handleDataSourceChange
    },
    {
      label: "Country",
      value: countryLabel,
      items: countries.map((c) => ({ label: c.label, value: c.slug })),
      onSelect: setCountrySlug
    },
    dataSource !== "Forecasts" && {
      label: "Data Type",
      value: dataTypeLabel,
      items: dataTypes.map((t) => ({ label: t.label, value: t.key })),
      onSelect: setDataTypeKey
    },
    {
      label: "Year Type",
      value: yearLabel,
      items: yearTypes.map((y) => ({ label: y.label, value: y.key })),
      onSelect: setYearType
    }
  ].filter(Boolean);

  return (
    <div className="main-content">
      <h2>{name}</h2>

      <div className="filter-bar-wrapper">
        <div className="filter-bar">
          {filters.map((f) => (
            <div className="filter-item" key={f.label}>
              <label>{f.label}</label>
              <Dropdown label={f.value} items={f.items} onSelect={f.onSelect} />
            </div>
          ))}
        </div>
      </div>

      {dataSource === "Forecasts" ? (
        <div className="card card-centered commodity-chart">
          <h3>Forecasts – Under Construction</h3>
          <div className="chart-area chart-area-placeholder">
            Forecasts are under construction.
          </div>
        </div>
      ) : (
        <div className="card card-centered commodity-chart">
          <h3>
            {dataSource} – {countryLabel} – {dataTypeLabel} – {yearLabel}
          </h3>
          <div className="chart-area">
            <ChartViewer
              jsonPath={`${process.env.REACT_APP_API_BASE}/${slug}/${dataSource.toLowerCase()}/${countrySlug}/${effectiveDataTypeKey}/${yearType}`}
              variant="commodity"
            />
          </div>
        </div>
      )}
    </div>
  );
}
