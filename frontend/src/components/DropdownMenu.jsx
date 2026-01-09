import React from "react";
import { useNavigate } from "react-router-dom";

export default function DropdownMenu({ items }) {
  const navigate = useNavigate();

  return (
    <div className="dropdown">
      {items.map((item, idx) => (
        <div
          key={idx}
          className="dropdown-item"
          onClick={() => navigate(item.to)}
        >
          {item.label}
        </div>
      ))}
    </div>
  );
}