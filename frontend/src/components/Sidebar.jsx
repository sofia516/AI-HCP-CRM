import { NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user"));

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <div className="logo">
        <h2>AI-HCP CRM</h2>
        <p>Healthcare Intelligence</p>
      </div>

      <div className="user-card">
        <div className="avatar">👤 </div>

   <h4>{user?.name}</h4>

   <p>{user?.email}</p>
   </div>

      <nav className="nav-menu">
        <NavLink to="/" end>
          📊 Dashboard
        </NavLink>

        <NavLink to="/hcps">
          👨‍⚕️ HCPs
        </NavLink>

        <NavLink to="/interactions">
          💬 Interactions
        </NavLink>

        <NavLink to="/ai-assistant">
          🤖 AI Assistant
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          🚪 Logout
        </button>

        <p>AI-powered CRM</p>
      </div>
    </aside>
  );
}

export default Sidebar;