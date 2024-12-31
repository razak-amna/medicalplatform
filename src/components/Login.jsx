// import React, { useState } from "react";
// import axios from "axios";
// import { useNavigate } from "react-router-dom";

// function Login() {
//   const [formData, setFormData] = useState({
//     username: "",
//     password: "",
//   });
//   const [error, setError] = useState("");
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   const handleSubmit = async (e) => {
//     // e.preventDefault(); // Prevent form from reloading

//     setError("");

//     try {
//       // Fetch CSRF token from cookies
//       const csrfToken = document.cookie
//         .split("; ")
//         .find((row) => row.startsWith("csrftoken"))
//         ?.split("=")[1];

//       // Send login request with credentials
//       await axios.post(
//         "http://127.0.0.1:8000/login/",
//         { username: formData.username, password: formData.password },
//         {
//           withCredentials: true,
//           headers: { "X-CSRFToken": csrfToken },
//         }
//       );

//       // Fetch user profile after login
//       const userProfileResponse = await axios.get("http://127.0.0.1:8000/profile/${userId}", {
//         withCredentials: true,
//       });

//       // Handle user profile data here (if needed)
//       console.log(userProfileResponse.data);

//       // Navigate to the profile page
//       navigate(`http://localhost:5173/profile/${userId}`);
//     } catch (error) {
//       console.error("Login error:", error.response ? error.response.data : error);
//       setError(error.response?.data?.detail || "Login failed. Please try again.");
//     }
//   };

//   return (
//     <div>
//       <h1>Login</h1>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="text"
//           name="username"
//           placeholder="Username"
//           value={formData.username}
//           onChange={handleChange}
//           required
//         />
//         <input
//           type="password"
//           name="password"
//           placeholder="Password"
//           value={formData.password}
//           onChange={handleChange}
//           required
//         />
//         <button type="submit">Login</button>
//       </form>
//       {error && <p style={{ color: "red" }}>{error}</p>}
//     </div>
//   );
// }

// export default Login;


import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Update form data as the user types
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form reload
    setError(""); // Clear previous error messages

    try {
      // Fetch CSRF token from cookies
      const csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken"))
        ?.split("=")[1];

      if (!csrfToken) {
        throw new Error("CSRF token not found. Please refresh the page.");
      }

      // Send login request to the backend
      const response = await axios.post(
        "http://127.0.0.1:8000/login/",
        { username: formData.username, password: formData.password },
        {
          withCredentials: true, // Include cookies in the request
          headers: { "X-CSRFToken": csrfToken }, // Attach CSRF token
        }
      );

      // On success, navigate to the user's profile
      const userId = response.data.userId; // Backend should return userId in the response
      console.log("Login successful:", response.data);
      navigate(`/profile/${userId}`); // Adjust the path as needed
    } catch (error) {
      console.error("Login error:", error.response ? error.response.data : error);
      setError(error.response?.data?.detail || "Login failed. Please try again.");
    }
  };

  return (
    <div>
      <h1>Login</h1>
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
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Login;
