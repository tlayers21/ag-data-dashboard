import { useState, useRef, useEffect } from "react";

export default function Dropdown({ label, items, onSelect }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  // Close when clicking anywhere outside the dropdown
  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div className="nav-item filter-dropdown" ref={ref}>
      <span className="nav-label filter-label" onClick={() => setOpen((o) => !o)}>
        {label} ▾
      </span>

      {open && (
        <div className="dropdown">
          {items.map((item) => (
            <div
              key={item.value}
              className="dropdown-item"
              onClick={() => {
                onSelect(item.value);
                setOpen(false);
              }}
            >
              {item.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
