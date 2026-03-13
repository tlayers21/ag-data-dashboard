import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import BackArrow from "./components/BackArrow";

import Home from "./pages/Home";
import About from "./pages/About";
import DataOverview from "./pages/DataOverview";

import Corn from "./pages/Corn";
import Ethanol from "./pages/Ethanol";

import Wheat from "./pages/Wheat";
import SRWWheat from "./pages/SRWWheat";
import HRWWheat from "./pages/HRWWheat";

import Soybeans from "./pages/Soybeans";
import SoybeanMeal from "./pages/SoybeanMeal";
import SoybeanOil from "./pages/SoybeanOil";

import "./App.css";

function App() {
  return (
    <>
      <Header />
      <Navbar />
      <div className="page-wrapper">
        <BackArrow />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/data-overview" element={<DataOverview />} />

          {/* Corn */}
          <Route path="/corn" element={<Corn />} />
          <Route path="/corn/inspections" element={<Corn />} />
          <Route path="/corn/esr" element={<Corn />} />
          <Route path="/corn/forecasts" element={<Corn />} />

          {/* Ethanol */}
          <Route path="/ethanol" element={<Ethanol />} />
          <Route path="/ethanol/forecasts" element={<Ethanol />} />

          {/* Wheat */}
          <Route path="/wheat" element={<Wheat />} />
          <Route path="/wheat/inspections" element={<Wheat />} />
          <Route path="/wheat/esr" element={<Wheat />} />
          <Route path="/wheat/forecasts" element={<Wheat />} />

          {/* SRW Wheat */}
          <Route path="/srw-wheat" element={<SRWWheat />} />
          <Route path="/srw-wheat/esr" element={<SRWWheat />} />
          <Route path="/srw-wheat/forecasts" element={<SRWWheat />} />

          {/* HRW Wheat */}
          <Route path="/hrw-wheat" element={<HRWWheat />} />
          <Route path="/hrw-wheat/esr" element={<HRWWheat />} />
          <Route path="/hrw-wheat/forecasts" element={<HRWWheat />} />

          {/* Soybeans */}
          <Route path="/soybeans" element={<Soybeans />} />
          <Route path="/soybeans/inspections" element={<Soybeans />} />
          <Route path="/soybeans/esr" element={<Soybeans />} />
          <Route path="/soybeans/forecasts" element={<Soybeans />} />

          {/* Soybean Meal */}
          <Route path="/soybean-meal" element={<SoybeanMeal />} />
          <Route path="/soybean-meal/esr" element={<SoybeanMeal />} />
          <Route path="/soybean-meal/forecasts" element={<SoybeanMeal />} />

          {/* Soybean Oil */}
          <Route path="/soybean-oil" element={<SoybeanOil />} />
          <Route path="/soybean-oil/esr" element={<SoybeanOil />} />
          <Route path="/soybean-oil/forecasts" element={<SoybeanOil />} />
        </Routes>
      </div>
    </>
  );
}

export default App;