import { useState, useEffect } from 'react';
import axios from 'axios';

const NotificationList = () => {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(''); // For storing error message
  const [loading, setLoading] = useState(true); // For handling loading state
  
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/notifications/')
      .then(response => {
        setNotifications(response.data);
        setLoading(false); // Hide loading state when data is fetched
      })
      .catch(error => {
        console.error('Error fetching notifications:', error);
        setError('Failed to load notifications');
        setLoading(false); // Hide loading state even if there's an error
      });
  }, []);
  
  if (loading) {
    return <p>Loading notifications...</p>; // Show loading text while fetching data
  }

  return (
    <div>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
      {notifications.length > 0 ? (
        notifications.map(notification => (
          <div key={notification.id}>
            <p>{notification.message}</p>
          </div>
        ))
      ) : (
        <p>No notifications available.</p> // Show message when no notifications
      )}
    </div>
  );
};

export default NotificationList;
