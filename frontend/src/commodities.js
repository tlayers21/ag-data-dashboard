export const INSPECTIONS_TYPES = [
  { key: "export_inspections", label: "Export Inspections" }
];

export const ESR_TYPES = [
  { key: "weekly_exports", label: "Weekly Exports" },
  { key: "accumulated_exports", label: "Accumulated Exports" },
  { key: "outstanding_sales", label: "Outstanding Sales" },
  { key: "gross_new_sales", label: "Gross New Sales" },
  { key: "current_marketing_year_net_sales", label: "Current Marketing Year Net Sales" },
  { key: "current_marketing_year_total_commitment", label: "Current Marketing Year Total Commitment" },
  { key: "next_marketing_year_net_sales", label: "Next Marketing Year Net Sales" },
  { key: "next_marketing_year_outstanding_sales", label: "Next Marketing Year Outstanding Sales" }
];

export const YEAR_TYPES = [
  { key: "my", label: "Marketing Year" },
  { key: "cal", label: "Calendar Year" }
];

export const BASE_COUNTRIES = [
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

// PSD also covers the U.S., listed right after World
export const PSD_COUNTRIES = [
  BASE_COUNTRIES[0],
  { label: "United States", slug: "united-states" },
  ...BASE_COUNTRIES.slice(1)
];

const PSD_LABELS = {
  area_harvested: "Area Harvested",
  crush: "Crush",
  beginning_stocks: "Beginning Stocks",
  production: "Production",
  imports: "Imports",
  trade_year_imports: "Trade Year Imports",
  trade_year_imports_from_united_states: "Trade Year Imports From U.S.",
  total_supply: "Total Supply",
  exports: "Exports",
  trade_year_exports: "Trade Year Exports",
  domestic_consumption: "Domestic Consumption",
  feed_domestic_consumption: "Feed Domestic Consumption",
  industrial_domestic_consumption: "Industrial Domestic Consumption",
  food_use_domestic_consumption: "Food Use Domestic Consumption",
  feed_waste_domestic_consumption: "Feed Waste Domestic Consumption",
  ending_stocks: "Ending Stocks",
  total_distribution: "Total Distribution",
  yield: "Yield",
  food_seed_and_industrial_consumption: "Food Seed and Industrial Consumption",
  extraction_rate: "Extraction Rate",
  soybean_meal_equivalent: "Soybean Meal Equivalent"
};

const psd = (keys) => keys.map((key) => ({ key, label: PSD_LABELS[key] }));

const GRAIN_PSD = psd([
  "area_harvested", "beginning_stocks", "production", "imports", "trade_year_imports",
  "trade_year_imports_from_united_states", "total_supply", "exports", "trade_year_exports",
  "domestic_consumption", "feed_domestic_consumption", "ending_stocks", "total_distribution",
  "yield", "food_seed_and_industrial_consumption"
]);

const SOYBEAN_PSD = psd([
  "area_harvested", "crush", "beginning_stocks", "production", "imports", "total_supply",
  "exports", "domestic_consumption", "food_use_domestic_consumption",
  "feed_waste_domestic_consumption", "ending_stocks", "total_distribution", "yield"
]);

const SOYBEAN_OIL_PSD = psd([
  "crush", "beginning_stocks", "production", "imports", "total_supply", "exports",
  "domestic_consumption", "industrial_domestic_consumption", "food_use_domestic_consumption",
  "feed_waste_domestic_consumption", "ending_stocks", "total_distribution", "extraction_rate"
]);

const SOYBEAN_MEAL_PSD = [...SOYBEAN_OIL_PSD, ...psd(["soybean_meal_equivalent"])];

const ALL_SOURCES = ["Inspections", "ESR", "PSD", "Forecasts"];

export const COMMODITIES = [
  { slug: "corn", name: "Corn", dataSources: ALL_SOURCES, psdAttributes: GRAIN_PSD },
  { slug: "wheat", name: "Wheat", dataSources: ALL_SOURCES, psdAttributes: GRAIN_PSD },
  { slug: "srw-wheat", name: "SRW Wheat", dataSources: ["ESR", "Forecasts"] },
  { slug: "hrw-wheat", name: "HRW Wheat", dataSources: ["ESR", "Forecasts"] },
  { slug: "soybeans", name: "Soybeans", dataSources: ALL_SOURCES, psdAttributes: SOYBEAN_PSD },
  { slug: "soybean-meal", name: "Soybean Meal", dataSources: ["ESR", "PSD", "Forecasts"], psdAttributes: SOYBEAN_MEAL_PSD },
  { slug: "soybean-oil", name: "Soybean Oil", dataSources: ["ESR", "PSD", "Forecasts"], psdAttributes: SOYBEAN_OIL_PSD }
];
