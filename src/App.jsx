import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import AppointmentList from './components/AppointmentList';
import FeedbackForm from './components/FeedbackForm';
import NotificationList from './components/NotificationList';
import DoctorList from './components/DoctorList';
import UserProfile from './components/UserProfile';
import Login from './components/Login';
import Navbar from './components/Navbar'; 
import Register from './components/Register';
import './styles/chatbot.css'; // Import the CSS for chatbot
import CreateDoctor from './components/CreateDoctor';
import CreateAppointment from './components/CreateAppointment';

function App() {
  return (
    <Router>
      <Navbar /> {/* Display Navbar at the top of the page */}
      <div style={styles.contentContainer}>
        <Routes>
          <Route path="/" element={<h1>Welcome to the Health Portal</h1>} />
          <Route path="/login" element={<Login />} />
          {/* Adjusted the UserProfile route to not require a userId in the URL */}
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/appointments" element={<AppointmentList />} />
          <Route path="/feedback" element={<FeedbackForm sessionId={1} />} />
          <Route path="/notifications" element={<NotificationList />} />
          <Route path="/doctors" element={<DoctorList />} />
          <Route path="/create-doctors" element={<CreateDoctor />} />
          <Route path="/create-appointments" element={<CreateAppointment />} />
          <Route path="*" element={<div>404: Page Not Found</div>} />
        </Routes>
      </div>
    </Router>
  );
}

const styles = {
  contentContainer: {
    display: 'flex',
    flexDirection: 'column', // For better control of vertical layout
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    textAlign: 'center',
  },
};

export default App;
