import "./styles/layout.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import SearchCustomer from "./components/SearchCustomer";
import AuthorizationsTable from "./components/AuthorizationsTable";
import FiltersPanel from "./components/FiltersPanel";
import TopMenu from "./components/TopMenu";
import CustomerDashboard from "./pages/CustomerDashboard";
import InvestmentPropensityDashboard from "./pages/InvestmentPropensityDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <TopMenu />

      <Routes>
        {/* Home / pagina principale */}
        <Route
          path="/"
          element={
            <div className="page-container container bg-white">
              <SearchCustomer />

              <div className="flex-row" style={{ alignItems: "flex-start" }}>
                <AuthorizationsTable />
                <FiltersPanel />
              </div>
            </div>
          }
        />

        {/* La pagina che vuoi mostrare → /dashboard/123 */}
        <Route path="/dashboard/:userId" element={<CustomerDashboard />} />
        <Route path="/investment-propensity" element={<InvestmentPropensityDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}