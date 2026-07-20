import { useEffect, useState } from "react";
import api from "../services/api";

function Interactions() {
  const [interactions, setInteractions] = useState([]);
  const [hcps, setHcps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    hcp_id: "",
    interaction_type: "",
    notes: "",
  });

  const fetchData = async () => {
    try {
      setLoading(true);

      const [interactionsResponse, hcpsResponse] =
        await Promise.all([
          api.get("/interactions/"),
          api.get("/hcps/"),
        ]);

      setInteractions(interactionsResponse.data);
      setHcps(hcpsResponse.data);
    } catch (error) {
      console.error(error);
      setMessage("Unable to load interaction data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const payload = {
        hcp_id: Number(formData.hcp_id),
        interaction_type: formData.interaction_type,
        notes: formData.notes,
      };

      await api.post("/interactions/", payload);

      setMessage("Interaction logged successfully.");

      setFormData({
        hcp_id: "",
        interaction_type: "",
        notes: "",
      });

      await fetchData();
    } catch (error) {
      console.error(error);
      setMessage("Unable to log interaction.");
    }
  };

  const getHcpName = (hcpId) => {
    const hcp = hcps.find(
      (item) => item.id === hcpId
    );

    return hcp ? hcp.name : `HCP ${hcpId}`;
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Interactions</h1>
          <p>
            Log and review interactions with healthcare
            professionals.
          </p>
        </div>
      </div>

      <div className="hcp-layout">
        <div className="form-card">
          <h2>Log Interaction</h2>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Healthcare Professional</label>

              <select
                name="hcp_id"
                value={formData.hcp_id}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select an HCP
                </option>

                {hcps.map((hcp) => (
                  <option
                    key={hcp.id}
                    value={hcp.id}
                  >
                    {hcp.name} — {hcp.specialty}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Interaction Type</label>

              <select
                name="interaction_type"
                value={formData.interaction_type}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select type
                </option>
                <option value="Visit">
                  Visit
                </option>
                <option value="Call">
                  Call
                </option>
                <option value="Email">
                  Email
                </option>
                <option value="Meeting">
                  Meeting
                </option>
                <option value="Follow-up Call">
                  Follow-up Call
                </option>
              </select>
            </div>

            <div className="form-group">
              <label>Notes</label>

              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                placeholder="Enter interaction details..."
                rows="6"
                required
              />
            </div>

            <button
              type="submit"
              className="primary-button"
            >
              Log Interaction
            </button>
          </form>

          {message && (
            <p className="form-message">
              {message}
            </p>
          )}
        </div>

        <div className="table-card">
          <div className="table-header">
            <h2>Interaction History</h2>

            <button
              className="secondary-button"
              onClick={fetchData}
            >
              Refresh
            </button>
          </div>

          {loading ? (
            <p>Loading interactions...</p>
          ) : interactions.length === 0 ? (
            <p>No interactions found.</p>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>HCP</th>
                    <th>Type</th>
                    <th>Notes</th>
                    <th>Date</th>
                  </tr>
                </thead>

                <tbody>
                  {interactions.map(
                    (interaction) => (
                      <tr key={interaction.id}>
                        <td>
                          {interaction.id}
                        </td>

                        <td>
                          {getHcpName(
                            interaction.hcp_id
                          )}
                        </td>

                        <td>
                          <span className="type-badge">
                            {
                              interaction.interaction_type
                            }
                          </span>
                        </td>

                        <td className="notes-cell">
                          {interaction.notes}
                        </td>

                        <td>
                          {interaction.created_at
                            ? new Date(
                                interaction.created_at
                              ).toLocaleString()
                            : "-"}
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Interactions;