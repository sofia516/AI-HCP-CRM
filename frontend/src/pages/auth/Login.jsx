import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // If already logged in, redirect to dashboard
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      navigate("/");
    }
  }, [navigate]);

  async function login(e) {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", {
        email,
        password,
      });

      console.log("Login Response:", res.data);

      localStorage.setItem(
        "access_token",
        res.data.access_token
      );

      localStorage.setItem(
        "user",
       JSON.stringify(res.data.user)
      );

      alert("Login Successful!");

      navigate("/");
    } catch (err) {
      console.error("Login Error:", err);

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
      <h1>AI-HCP CRM Login</h1>

      <form onSubmit={login}>
        <input
          type="email"
          placeholder="Email"
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
          Login
        </button>
      </form>

      <p style={{ marginTop: "20px", textAlign: "center" }}>
        Don't have an account?{" "}
        <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}

export default Login;