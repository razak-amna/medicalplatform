// src/components/FeedbackForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

const FeedbackForm = () => {
  const [feedbackText, setFeedbackText] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFeedbackText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate feedback text before submission
    if (!feedbackText.trim()) {
      setError('Feedback cannot be empty.');
      return;
    }

    // Optionally, get the token from localStorage or some other means
    const token = localStorage.getItem('authToken');
    
    axios
      .post(
        'http://127.0.0.1:8000/feedback/', 
        { feedbackText },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        console.log('Feedback submitted:', response.data);
        setMessage('Thank you for your feedback!');
        setFeedbackText(''); // Clear feedback text after submission
        setError(''); // Clear error if submission is successful
      })
      .catch((error) => {
        console.error('Error submitting feedback:', error);
        setError('Failed to submit feedback. Please try again.');
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Feedback:</label>
        <textarea
          name="feedback"
          value={feedbackText}
          onChange={handleChange}
        />
      </div>
      <button type="submit">Submit</button>
      
      {/* Display success or error message */}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
};

export default FeedbackForm;
