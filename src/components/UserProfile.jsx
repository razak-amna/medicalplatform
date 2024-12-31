import React, { useEffect, useState } from 'react';
import axios from 'axios';

// Reusable Section Component
const Section = ({ title, content }) => (
  <div>
    <h3>{title}</h3>
    {content ? (
      Array.isArray(content) ? (
        <ul>
          {content.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>{content}</p>
      )
    ) : (
      <p>No data available.</p>
    )}
  </div>
);

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch user details after login (you can use cookies or session to authenticate)
    axios.get("http://127.0.0.1:8000/profile/${userId}/", { withCredentials: true })
      .then(response => {
        setUserData(response.data); // Save user data
      })
      .catch(err => {
        setError(err.response?.data?.detail || "Failed to fetch user details.");
        console.error("Error fetching user details:", err);
      });
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  if (!userData) {
    return <div>Loading...</div>;
  }

  const { username, email, dob, gender, phone_number, address, medical_history, appointments, chat_history } = userData;

  return (
    <div>
      <h1>Your Profile</h1>
      <p><strong>Username:</strong> {username}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Date of Birth:</strong> {dob || "Not provided"}</p>
      <p><strong>Gender:</strong> {gender || "Not provided"}</p>
      <p><strong>Phone Number:</strong> {phone_number || "Not provided"}</p>
      <p><strong>Address:</strong> {address || "Not provided"}</p>

      {/* Reusable Section Components */}
      <Section
        title="Medical History"
        content={medical_history ? Object.entries(medical_history).map(([key, value]) => `${key}: ${value}`) : null}
      />
      <Section
        title="Appointments"
        content={appointments ? appointments.map((appointment, index) => (
          `${appointment.doctor_name} on ${appointment.date} - ${appointment.status}`
        )) : null}
      />
      <Section
        title="Chat History"
        content={chat_history ? chat_history.map((chat, index) => (
          `${chat.chat_type}: ${chat.message} at ${chat.timestamp}`
        )) : null}
      />
    </div>
  );
};

export default UserProfile;
