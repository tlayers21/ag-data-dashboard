import React from "react";

export default function DropdownMenu({ items, onSelect }) {
  return (
    <div className="dropdown">
      {items.map((item, idx) => (
        <div
          key={idx}
          className="dropdown-item"
          onClick={() => onSelect(item.value)}
        >
          {item.label}
        </div>
      ))}
    </div>
  );
}