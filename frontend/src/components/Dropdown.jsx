import { useState, useRef, useEffect } from "react";
import DropdownMenu from "./DropdownMenu";

export default function Dropdown({ label, items, onSelect }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

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
      <span
        className="nav-label filter-label"
        onClick={() => setOpen((o) => !o)}
      >
        {label} ▾
      </span>

      {open && (
        <DropdownMenu
          items={items}
          onSelect={(value) => {
            onSelect(value);
            setOpen(false);
          }}
        />
      )}
    </div>
  );
}