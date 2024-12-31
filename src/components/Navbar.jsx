// src/components/Navbar.jsx
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={styles.navbar}>
      <ul style={styles.navList}>
        <li style={styles.navItem}>
          <Link to="/" style={styles.navLink}>Home</Link>
        </li>
        <li style={styles.navItem}>
          <Link to="/login" style={styles.navLink}>Login</Link>
        </li>
        <li style={styles.navItem}>
          <Link to="/register" style={styles.navLink}>Register</Link>
        </li>
        <li style={styles.navItem}>
          <Link to="/profile" style={styles.navLink}>Profile</Link>
        </li>
      </ul>
    </nav>
  );
}

const styles = {
  navbar: {
    backgroundColor: '#333',
    padding: '10px 20px',
  },
  navList: {
    display: 'flex',
    justifyContent: 'space-around',
    listStyleType: 'none',
    padding: 0,
  },
  navItem: {
    margin: '0 10px',
  },
  navLink: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '18px',
  },
};

export default Navbar;
