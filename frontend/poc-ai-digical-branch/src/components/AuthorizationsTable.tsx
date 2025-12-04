import "../styles/layout.css";

export default function AuthorizationsTable() {
  return (
    <div className="card" style={{ flex: 1, minHeight: "500px"}}>
      <h2 className="section-title">Authorizations (0)</h2>

      <p style={{ color: "#6b7280", fontSize: "14px", marginBottom: "16px" }}>
        Refresh data frequently in order to update the authorizations list
      </p>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Relationship Manager</th>
              <th>Customer</th>
              <th>Approval Type</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
        </table>
      </div>
    </div>
  );
}
