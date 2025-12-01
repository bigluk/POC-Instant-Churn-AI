import "../styles/layout.css";

export default function FiltersPanel() {
  return (
    <div className="card" style={{ width: "350px", minHeight: "500px"}}>
      <h2 className="section-title">Authorizations view</h2>
      <p style={{ color: "#6b7280", fontSize: "14px", marginBottom: "20px" }}>
        Filter authorization view
      </p>

      <div className="filter-group">
        <label className="filter-label">
          <input type="checkbox" /> RM
        </label>
        <select className="input">
          <option>Select</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">
          <input type="checkbox" /> Description
        </label>
        <select className="input">
          <option>Select</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">
          <input type="checkbox" /> Status
        </label>
        <select className="input">
          <option>Select</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">
          <input type="checkbox" /> Date
        </label>
        <input type="date" className="input" />
      </div>
    </div>
  );
}
