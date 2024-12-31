import React, { useState } from 'react';
import axios from 'axios';

const CreateDoctor = () => {
  const [doctorData, setDoctorData] = useState({
    name: '',
    specialization: '',
    availability: true,
  });
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setDoctorData({
      ...doctorData,
      [e.target.name]: e.target.value,
    });
  };

  const getCSRFToken = () => {
    // Get the CSRF token from cookies
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    return csrfToken;
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent form submission from refreshing the page
    setError(""); // Clear any previous error messages
    setMessage(""); // Clear any previous success messages

    const csrfToken = getCSRFToken();

    if (!csrfToken) {
      setError("CSRF token missing");
      return;
    }

    
    try {

      // Send the CSRF token along with the doctor data
      const response = await axios.post(
        'http://127.0.0.1:8000/create-doctors/', // Endpoint to add doctor
        doctorData, 
        {
          headers: {
            'X-CSRFToken': csrfToken,  // Send the CSRF token in the headers
            'Content-Type': 'application/json',  // Sending JSON data
          },
          withCredentials: true,  // Include credentials if required by the backend
        }
      );

      setMessage('Doctor added successfully!');
      // Handle further actions after success (like clearing the form or redirecting)
      console.log(response.data);
    } catch (error) {
      console.error('Error adding doctor:', error);
      setError(error.response?.data?.detail || 'Error adding doctor.');
    }
  };

  return (
    <div>
      <h1>Create Doctor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Doctor's Name"
          value={doctorData.name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="specialization"
          placeholder="Specialization"
          value={doctorData.specialization}
          onChange={handleChange}
          required
        />
        <label>
          Available:
          <input
            type="checkbox"
            name="availability"
            checked={doctorData.availability}
            onChange={(e) =>
              setDoctorData({ ...doctorData, availability: e.target.checked })
            }
          />
        </label>
        <button type="submit">Add Doctor</button>
      </form>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default CreateDoctor;
