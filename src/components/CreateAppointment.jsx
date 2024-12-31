import React, { useState } from 'react';
import axios from 'axios';

function CreateAppointment() {
  const [doctor, setDoctor] = useState('');
  const [patient, setPatient] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validate that all fields are filled
    if (!doctor || !patient || !date || !time || !status) {
      setError('All fields are required.');
      return;
    }

    const token = localStorage.getItem('authToken'); // Get the token from localStorage
    if (!token) {
      setError('User not authenticated.');
      return;
    }

    try {
      // Combine date and time into one string if necessary for the backend
      const appointmentDateTime = `${date}T${time}:00`; // ISO format (e.g. "2024-12-30T14:00:00")

      const response = await axios.post(
        'http://127.0.0.1:8000/create-appointments/', 
        {
          doctor,
          patient,
          appointment_date: appointmentDateTime, // Send combined date and time
          status,
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setSuccess('Appointment created successfully!');
      console.log('Appointment created:', response.data);

      // Optionally, clear the form fields after success
      setDoctor('');
      setPatient('');
      setDate('');
      setTime('');
      setStatus('');
      setError('');
    } catch (err) {
      console.error('Error creating appointment:', err.response ? err.response.data : err.message);
      setError(err.response?.data?.detail || 'Error creating appointment');
    }
  };

  return (
    <div>
      <h1>Create Appointment</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Doctor ID"
          value={doctor}
          onChange={(e) => setDoctor(e.target.value)}
        />
        <input
          type="text"
          placeholder="Patient ID"
          value={patient}
          onChange={(e) => setPatient(e.target.value)}
        />
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <input
          type="time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
        />
        <input
          type="text"
          placeholder="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        />
        <button type="submit">Create Appointment</button>
      </form>
    </div>
  );
}

export default CreateAppointment;
