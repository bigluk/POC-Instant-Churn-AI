import "./styles/layout.css";

import SearchCustomer from "./components/SearchCustomer";
import AuthorizationsTable from "./components/AuthorizationsTable";
import FiltersPanel from "./components/FiltersPanel";
import TopMenu from "./components/TopMenu";

export default function App() {
  return (
    <div>
      <TopMenu />
      <div className="page-container container">
        <SearchCustomer />

        <div className="flex-row" style={{ alignItems: "flex-start" }}>
          <AuthorizationsTable />
          <FiltersPanel />
        </div>
      </div>
    </div>
  );
}