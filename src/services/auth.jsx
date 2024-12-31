import axios from 'axios';

// Base URL for your API
const BASE_URL = 'http://127.0.0.1:8000';

// Login function
export const login = async (username, password) => {
  try {
    const response = await axios.post(`${BASE_URL}http://127.0.0.1:8000/token/`, {
      username,
      password,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data; // Return the token data for further use if needed
  } catch (error) {
    console.error('Login failed:', error);
    throw error; // Propagate error for handling in the component
  }
};
