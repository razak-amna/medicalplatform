import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AppointmentList = () => {
  const [doctors, setDoctors] = useState([]);
  const [appointmentData, setAppointmentData] = useState({
    reason: '',
    doctorId: '',
    appointmentDate: '',
  });
  const [createdAppointment, setCreatedAppointment] = useState(null);
  const [error, setError] = useState('');

  // Fetch doctor list on component mount
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/doctors/')
      .then(response => {
        setDoctors(response.data);
      })
      .catch(error => {
        console.error('Error fetching doctors:', error);
      });
  }, []);

  // Handle form data changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setAppointmentData({
      ...appointmentData,
      [name]: value,
    });
  };

  // Handle appointment creation
  const handleSubmit = (e) => {
    e.preventDefault();
  
    // Ensure all fields are filled
    if (!appointmentData.reason || !appointmentData.doctorId || !appointmentData.appointmentDate) {
      setError("All fields are required.");
      return;
    }
  
    axios.post('http://127.0.0.1:8000/appointments/', {
      reason: appointmentData.reason,
      doctorId: appointmentData.doctorId,
      appointmentDate: appointmentData.appointmentDate, // Must be in ISO 8601 format
    })
      .then(response => {
        console.log('Appointment created successfully:', response.data);
        setCreatedAppointment(response.data);  // Update the state with the created appointment data
        setError('');
        // Optionally reset the form
        setAppointmentData({
          reason: '',
          doctorId: '',
          appointmentDate: '',
        });
      })
      .catch(error => {
        console.error('Error creating appointment:', error);
        setError(error.response?.data?.detail || 'Failed to create appointment.');
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Reason for Appointment:</label>
          <input
            type="text"
            name="reason"
            value={appointmentData.reason}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Doctor:</label>
          <select
            name="doctorId"
            value={appointmentData.doctorId}
            onChange={handleChange}
          >
            <option value="">Select a doctor</option>
            {doctors.map((doctor) => (
              <option key={doctor.id} value={doctor.id}>
                {doctor.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Appointment Date:</label>
          <input
            type="datetime-local"
            name="appointmentDate"
            value={appointmentData.appointmentDate}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>

      {/* Display created appointment details */}
      {createdAppointment && (
        <div>
          <h3>Appointment Created Successfully!</h3>
          <p><strong>Appointment ID:</strong> {createdAppointment.id}</p>
          <p><strong>Doctor:</strong> {createdAppointment.doctor_name}</p>
          <p><strong>Reason:</strong> {createdAppointment.reason}</p>
          <p><strong>Appointment Date:</strong> {new Date(createdAppointment.appointmentDate).toLocaleString()}</p>
          <p><strong>Status:</strong> {createdAppointment.status}</p>
        </div>
      )}

      {/* Display error if appointment creation fails */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default AppointmentList;
