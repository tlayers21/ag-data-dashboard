import { Link } from "react-router-dom";
import "../App.css";

const menuItems = [
  {
    label: "Corn",
    items: [
      { label: "Corn", to: "/corn" },
      { label: "Ethanol", to: "/ethanol" }
    ]
  },
  {
    label: "Wheat",
    items: [
      { label: "Wheat (All)", to: "/wheat" },
      { label: "SRW Wheat", to: "/srw-wheat" },
      { label: "HRW Wheat", to: "/hrw-wheat" }
    ]
  },
  {
    label: "Soybeans",
    items: [
      { label: "Soybeans", to: "/soybeans" },
      { label: "Soybean Meal", to: "/soybean-meal" },
      { label: "Soybean Oil", to: "/soybean-oil" }
    ]
  }
];

export default function Navbar() {
  return (
    <nav className="navbar">
      <ul className="nav-list">

        {/* HOME BUTTON */}
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>

        {/* COMMODITY FAMILIES */}
        {menuItems.map((group) => (
          <li className="nav-item" key={group.label}>
            <span className="nav-label">{group.label} ▾</span>

            <ul className="dropdown">
              {group.items.map((item) => (
                <li className="dropdown-item" key={item.label}>
                  <Link to={item.to}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </li>
        ))}

        {/* ABOUT BUTTON */}
        <li className="nav-item">
          <Link to="/about" className="nav-link">About</Link>
        </li>

      </ul>
    </nav>
  );
}