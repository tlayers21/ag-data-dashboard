import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import BackArrow from "./components/BackArrow";

import Home from "./pages/Home";
import About from "./pages/About";
import DataOverview from "./pages/DataOverview";
import Ethanol from "./pages/Ethanol";
import CommodityPage from "./pages/CommodityPage";
import { COMMODITIES } from "./commodities";

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
          <Route path="/ethanol/*" element={<Ethanol />} />

          {/* key gives each commodity fresh filter state when switching between them */}
          {COMMODITIES.map((c) => (
            <Route
              key={c.slug}
              path={`/${c.slug}/*`}
              element={<CommodityPage key={c.slug} {...c} />}
            />
          ))}
        </Routes>
      </div>
    </>
  );
}

export default App;
