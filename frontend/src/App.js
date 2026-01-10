import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import BackArrow from "./components/BackArrow";

import Home from "./pages/Home";
import About from "./pages/About";
import Placeholder from "./pages/Placeholder";

import Corn from "./pages/Corn";
import Ethanol from "./pages/Ethanol";

import Wheat from "./pages/Wheat";
import SRWWheat from "./pages/SRWWheat";
import HRWWheat from "./pages/HRWWheat";

import Soybeans from "./pages/Soybeans";
import SoybeanMeal from "./pages/SoybeanMeal";
import SoybeanOil from "./pages/SoybeanOil";

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

          {/* Corn */}
          <Route path="/corn" element={<Corn />} />
          <Route path="/corn/inspections" element={<Placeholder />} />
          <Route path="/corn/esr" element={<Placeholder />} />
          <Route path="/corn/psd" element={<Placeholder />} />
          <Route path="/corn/forecasts" element={<Placeholder />} />
          <Route path="/ethanol" element={<Ethanol />} />
          <Route path="/ethanol/forecasts" element={<Placeholder />} />

          {/* Wheat */}
          <Route path="/wheat" element={<Wheat />} />
          <Route path="/wheat/inspections" element={<Placeholder />} />
          <Route path="/wheat/esr" element={<Placeholder />} />
          <Route path="/wheat/psd" element={<Placeholder />} />
          <Route path="/wheat/forecasts" element={<Placeholder />} />
          <Route path="/srw-wheat" element={<SRWWheat />} />
          <Route path="/srw-wheat/esr" element={<Placeholder />} />
          <Route path="/srw-wheat/psd" element={<Placeholder />} />
          <Route path="/srw-wheat/forecasts" element={<Placeholder />} />
          <Route path="/hrw-wheat" element={<HRWWheat />} />
          <Route path="/hrw-wheat/esr" element={<Placeholder />} />
          <Route path="/hrw-wheat/psd" element={<Placeholder />} />
          <Route path="/hrw-wheat/forecasts" element={<Placeholder />} />

          {/* Soybeans */}
          <Route path="/soybeans" element={<Soybeans />} />
          <Route path="/soybeans/inspections" element={<Placeholder />} />
          <Route path="/soybeans/esr" element={<Placeholder />} />
          <Route path="/soybeans/psd" element={<Placeholder />} />
          <Route path="/soybeans/forecasts" element={<Placeholder />} />
          <Route path="/soybean-meal" element={<SoybeanMeal />} />
          <Route path="/soybean-meal/esr" element={<Placeholder />} />
          <Route path="/soybean-meal/psd" element={<Placeholder />} />
          <Route path="/soybean-meal/forecasts" element={<Placeholder />} />
          <Route path="/soybean-oil" element={<SoybeanOil />} />
          <Route path="/soybean-oil/esr" element={<Placeholder />} />
          <Route path="/soybean-oil/psd" element={<Placeholder />} />
          <Route path="/soybean-oil/forecasts" element={<Placeholder />} />
        </Routes>
      </div>
    </>
  );
}

export default App;