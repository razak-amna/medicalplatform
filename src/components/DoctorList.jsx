import React, { useState, useEffect } from "react";
import axios from "axios";  // Import axios

function DoctorList() {
  const [doctors, setDoctors] = useState([]);  // State to store doctor data
  const [error, setError] = useState("");  // State to store any error messages
  const [loading, setLoading] = useState(true);  // State to track loading status

  useEffect(() => {
    const token = localStorage.getItem("authToken");  // Retrieve auth token from local storage

    if (!token) {
      setError("User not authenticated.");  // If no token is found, show an error
      setLoading(false);
      return;
    }

    console.log("Token:", token);  // Log the token for debugging purposes

    axios
      .get("http://127.0.0.1:8000/doctors/", {
        headers: {
          "Authorization": `Bearer ${token}`,  // Include token in the Authorization header
          "Content-Type": "application/json",  // Specify the content type as JSON
        },
      })
      .then((response) => {
        console.log("Doctors data:", response.data);  // Log the data for debugging
        setDoctors(response.data);  // Update the state with the doctor data
        setLoading(false);  // Set loading to false once data is fetched
      })
      .catch((err) => {
        console.error("Error fetching doctors:", err);
        setError("Failed to fetch doctors.");  // Show an error message
        setLoading(false);  // Set loading to false after error
      });

    // Cleanup function to avoid setting state on unmounted component
    return () => setLoading(false);
  }, []);  // Empty dependency array to only run once on mount

  return (
    <div>
      <h1>Available Doctors</h1>
      
      {loading && <p>Loading...</p>}  {/* Show loading message while fetching data */}
      
      {error && <p style={{ color: "red" }}>{error}</p>}  {/* Display error if any */}
      
      {!loading && doctors.length > 0 ? (
        <ul>
          {doctors.map((doctor) => (
            <li key={doctor.id}>
              <h3>{doctor.name}</h3>
              <p>{doctor.specialization}</p>
              <p>{doctor.availability ? "Available" : "Not Available"}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No doctors available.</p>  /* Display message if no doctors */
      )}
    </div>
  );
}

export default DoctorList;
