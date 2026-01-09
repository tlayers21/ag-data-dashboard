import React, { useState } from "react";
import DropdownMenu from "./DropdownMenu";
import { useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const [openMenu, setOpenMenu] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Helper: check if current path starts with something
  const isActive = (path) => location.pathname.startsWith(path);

  const menuItems = {
    corn: [
      { label: "ESR Data", to: "/corn/esr" },
      { label: "PSD Data", to: "/corn/psd" },
      { label: "Forecasts", to: "/corn/forecasts" }
    ],
    wheat: [
      { label: "ESR Data", to: "/wheat/esr" },
      { label: "PSD Data", to: "/wheat/psd" },
      { label: "Forecasts", to: "/wheat/forecasts" }
    ],
    soybeans: [
      { label: "ESR Data", to: "/soybeans/esr" },
      { label: "PSD Data", to: "/soybeans/psd" },
      { label: "Forecasts", to: "/soybeans/forecasts" }
    ]
  };

  return (
    <nav className="navbar">
      <div className="nav-center">

        {/* HOME BUTTON */}
        <button
          className="nav-button"
          onClick={() => navigate("/")}
          style={{
            fontWeight: location.pathname === "/" ? "bold" : "normal"
          }}
        >
          Home
        </button>

        {/* CORN / WHEAT / SOYBEANS */}
        {["corn", "wheat", "soybeans"].map((commodity) => (
          <div
            key={commodity}
            className="nav-item"
            onMouseEnter={() => setOpenMenu(commodity)}
            onMouseLeave={() => setOpenMenu(null)}
          >
            <button
              className="nav-button"
              style={{
                fontWeight: isActive(`/${commodity}`) ? "bold" : "normal"
              }}
            >
              {commodity.charAt(0).toUpperCase() + commodity.slice(1)}
            </button>

            {openMenu === commodity && (
              <DropdownMenu items={menuItems[commodity]} />
            )}
          </div>
        ))}

        {/* ABOUT ME */}
        <button
          className="nav-button"
          onClick={() => navigate("/about")}
          style={{
            fontWeight: location.pathname === "/about" ? "bold" : "normal"
          }}
        >
          About Me
        </button>
      </div>
    </nav>
  );
}