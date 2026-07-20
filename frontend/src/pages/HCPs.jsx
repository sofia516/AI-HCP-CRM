import { useEffect, useState } from "react";
import api from "../services/api";

function HCPs() {
  const [hcps, setHcps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    specialty: "",
    hospital: "",
    email: "",
    phone: "",
  });

  const fetchHcps = async () => {
    try {
      setLoading(true);

      const response = await api.get("/hcps/");

      setHcps(response.data);
    } catch (error) {
      console.error(error);
      setMessage("Unable to load HCPs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHcps();
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
      await api.post("/hcps/", formData);

      setMessage("HCP created successfully.");

      setFormData({
        name: "",
        specialty: "",
        hospital: "",
        email: "",
        phone: "",
      });

      fetchHcps();
    } catch (error) {
      console.error(error);

      if (error.response?.status === 409) {
        setMessage(
          " An HCP with this email already exists."
        );
      } else {
        setMessage("Unable to create HCP.");
      }
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Healthcare Professionals</h1>
          <p>Manage your HCP records and contact information.</p>
        </div>
      </div>

      <div className="hcp-layout">
        <div className="form-card">
          <h2>Add HCP</h2>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Dr. Rajesh Sharma"
                required
              />
            </div>

            <div className="form-group">
              <label>Specialty</label>
              <input
                type="text"
                name="specialty"
                value={formData.specialty}
                onChange={handleChange}
                placeholder="Cardiology"
                required
              />
            </div>

            <div className="form-group">
              <label>Hospital</label>
              <input
                type="text"
                name="hospital"
                value={formData.hospital}
                onChange={handleChange}
                placeholder="Apollo Hospital"
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="doctor@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label>Phone</label>
              <input
                type="text"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+91 9876543210"
                required
              />
            </div>

            <button type="submit" className="primary-button">
              Add HCP
            </button>
          </form>

          {message && (
            <p className="form-message">{message}</p>
          )}
        </div>

        <div className="table-card">
          <div className="table-header">
            <h2>All HCPs</h2>

            <button
              className="secondary-button"
              onClick={fetchHcps}
            >
              Refresh
            </button>
          </div>

          {loading ? (
            <p>Loading HCPs...</p>
          ) : hcps.length === 0 ? (
            <p>No HCPs found.</p>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Specialty</th>
                    <th>Hospital</th>
                    <th>Email</th>
                    <th>Phone</th>
                  </tr>
                </thead>

                <tbody>
                  {hcps.map((hcp) => (
                    <tr key={hcp.id}>
                      <td>{hcp.id}</td>
                      <td>{hcp.name}</td>
                      <td>{hcp.specialty}</td>
                      <td>{hcp.hospital}</td>
                      <td>{hcp.email}</td>
                      <td>{hcp.phone}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default HCPs;