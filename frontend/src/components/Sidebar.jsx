import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        <h2>AI-HCP CRM</h2>
        <p>Healthcare Intelligence</p>
      </div>

      <nav className="nav-menu">
        <NavLink to="/" end>
          Dashboard
        </NavLink>

        <NavLink to="/hcps">
          HCPs
        </NavLink>

        <NavLink to="/interactions">
          Interactions
        </NavLink>

        <NavLink to="/ai-assistant">
          AI Assistant
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <p>AI-powered CRM</p>
      </div>
    </aside>
  );
}

export default Sidebar;