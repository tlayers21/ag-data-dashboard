export default function Card({ title }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <div style={{ height: "200px", display: "flex", alignItems: "center", justifyContent: "center", color: "#777" }}>
        Placeholder Chart Area
      </div>
    </div>
  );
}