import { useState } from "react";
import "../styles/layout.css";
import { useNavigate } from "react-router-dom";

export default function SearchCustomer() {
  const [customerId, setCustomerId] = useState("");
  const navigate = useNavigate();


  const handleSearch = () => {
    if (customerId.trim() !== "") {
      navigate(`/dashboard/${customerId}`);
    }
  };

  return (
    <div className="card">
      <h2 className="section-title">Search customer</h2>

      <div className="grid-5">
        <label className="filter-label">
          <input type="checkbox" defaultChecked /> Session with customer
        </label>

        <input
          className="input"
          placeholder="Customer ID"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
        />
        <input className="input" placeholder="Surname" />
        <input className="input" placeholder="Name" />
        <input className="input" placeholder="Birth number" />
      </div>

      <div className="grid-2" style={{ marginTop: "16px" }}>
        <select className="input">
          <option>Identity Document</option>
        </select>

        <div className="flex-row" style={{ alignItems: "center" }}>
          <input className="input" placeholder="Document number" />
          <button className="btn" onClick={handleSearch}>Search</button>
        </div>
      </div>
    </div>
  );
}
