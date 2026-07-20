import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState({
    hcps: 0,
    interactions: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [hcpResponse, interactionResponse] =
          await Promise.all([
            api.get("/hcps/"),
            api.get("/interactions/"),
          ]);

        setStats({
          hcps: hcpResponse.data.length,
          interactions: interactionResponse.data.length,
        });
      } catch (error) {
        console.error(
          "Unable to load dashboard data:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>
            Welcome to your AI-powered Healthcare CRM.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span>Total HCPs</span>

          <h2>
            {loading ? "..." : stats.hcps}
          </h2>

          <p>Healthcare professionals</p>
        </div>

        <div className="stat-card">
          <span>Total Interactions</span>

          <h2>
            {loading ? "..." : stats.interactions}
          </h2>

          <p>Recorded CRM interactions</p>
        </div>

        <div className="stat-card">
          <span>AI Assistant</span>

          <h2>Active</h2>

          <p>Powered by Groq + LangGraph</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>AI-HCP CRM</h2>

        <p>
          Your AI-first Healthcare Professional CRM
          combines traditional relationship management
          with intelligent automation.
        </p>

        <div className="feature-grid">
          <div className="feature-item">
            <h3>HCP Management</h3>
            <p>
              Store and manage healthcare professional
              profiles and contact information.
            </p>
          </div>

          <div className="feature-item">
            <h3>Interaction Tracking</h3>
            <p>
              Record visits, calls, meetings, emails,
              and follow-up conversations.
            </p>
          </div>

          <div className="feature-item">
            <h3>AI Intelligence</h3>
            <p>
              Use natural language to log, edit, search,
              summarize, and analyze CRM interactions.
            </p>
          </div>

          <div className="feature-item">
            <h3>Smart Follow-ups</h3>
            <p>
              Generate context-aware follow-up
              recommendations from interaction history.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;