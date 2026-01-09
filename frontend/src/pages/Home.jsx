import Card from "../components/Card";

export default function Home() {
  return (
    <div className="main-content">

      <h2>Recent Corn Charts</h2>
      <div className="card-grid">
        <Card title="Weekly Exports" />
        <Card title="Cumulative Exports" />
        <Card title="Export Pace" />
      </div>

      <h2 style={{ marginTop: "3rem" }}>Recent Wheat Charts</h2>
      <div className="card-grid">
        <Card title="Weekly Exports" />
        <Card title="Cumulative Exports" />
        <Card title="Export Pace" />
      </div>

      <h2 style={{ marginTop: "3rem" }}>Recent Soybean Charts</h2>
      <div className="card-grid">
        <Card title="Weekly Exports" />
        <Card title="Cumulative Exports" />
        <Card title="Export Pace" />
      </div>

    </div>
  );
}