import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../../services/api";

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Redirect to dashboard if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      navigate("/");
    }
  }, [navigate]);

  async function register(e) {
    e.preventDefault();

    try {
      await api.post("/auth/register", {
        name,
        email,
        password,
      });

      alert("Registration Successful!");

      navigate("/login");
    } catch (err) {
      console.error("Registration Error:", err);

      if (err.response) {
        alert(
          `Error ${err.response.status}\n\n${JSON.stringify(
            err.response.data,
            null,
            2
          )}`
        );
      } else {
        alert("Unable to connect to the server.");
      }
    }
  }

  return (
    <div className="container">
      <h1>Create Account</h1>

      <form onSubmit={register}>
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
          Register
        </button>
      </form>

      <p style={{ marginTop: "20px", textAlign: "center" }}>
        Already have an account?{" "}
        <Link to="/login">Login here</Link>
      </p>
    </div>
  );
}

export default Register;