import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

const getAuthHeader = () => {
  const token = localStorage.getItem('access_token'); // Ensure the token is stored securely
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const fetchAppointments = async () => {
  return axios.get(`${BASE_URL}/api/appointments/`, {
    headers: getAuthHeader(),
  });
};

export const createAppointment = async (data) => {
  return axios.post(`${BASE_URL}/api/appointments/`, data, {
    headers: getAuthHeader(),
  });
};

