import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import About from "./pages/About";
import Placeholder from "./pages/Placeholder";

function App() {
  return (
    <>
      <Header />
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />

        {/* Corn */}
        <Route path="/corn/inspections" element={<Placeholder />} />
        <Route path="/corn/esr" element={<Placeholder />} />
        <Route path="/corn/psd" element={<Placeholder />} />
        <Route path="/corn/forecasts" element={<Placeholder />} />

        {/* Wheat */}
        <Route path="/wheat/inspections" element={<Placeholder />} />
        <Route path="/wheat/esr" element={<Placeholder />} />
        <Route path="/wheat/psd" element={<Placeholder />} />
        <Route path="/wheat/forecasts" element={<Placeholder />} />

        {/* Soybeans */}
        <Route path="/soybeans/inspections" element={<Placeholder />} />
        <Route path="/soybeans/esr" element={<Placeholder />} />
        <Route path="/soybeans/psd" element={<Placeholder />} />
        <Route path="/soybeans/forecasts" element={<Placeholder />} />
      </Routes>
    </>
  );
}

export default App;