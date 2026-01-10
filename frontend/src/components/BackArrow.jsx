import { useNavigate, useLocation } from "react-router-dom";

export default function BackArrow() {
  const navigate = useNavigate();
  const location = useLocation();

  if (location.pathname === "/") return null;

  return (
    <div className="back-arrow" onClick={() => navigate(-1)}>
      <span style={{ fontSize: "1.4rem" }}>←</span>
      <span>Back</span>
    </div>
  );
}