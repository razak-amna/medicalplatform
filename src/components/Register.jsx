import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // State to handle loading
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent form submission from refreshing the page
    setMessage(""); // Clear any previous messages
    setError(""); // Clear any previous errors
    setLoading(true); // Set loading state to true

    try {
      const response = await axios.post("http://127.0.0.1:8000/register/", formData);
      // Log the response to verify its structure
      console.log("Server Response:", response.data);
      setMessage("Registration successful! Redirecting to login...");
      setTimeout(() => {
        navigate("/login"); // Redirect to login after 2 seconds
      }, 1000);
    } catch (error) {
      // Handle error by setting the error message
      console.error("Registration error:", error.response?.data || error.message);
      setError(error.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false); // Set loading state to false after the process is done
    }
  };

  return (
    <div>
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Register;
