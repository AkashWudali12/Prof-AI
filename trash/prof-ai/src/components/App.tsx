// App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatBox from './HomePage';  // Assume HomePage.tsx is another component like About.tsx
import EmailDisplay from './GenEmailPage';
import TextImageList from './TextImageList';
import './styles/ChatBox.css';
import RegisterForm from './RegisterForm';
import LoginForm from './LoginForm'; 

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/browse_profs">Browse Professors</Link></li>
            <li><Link to="/get_email">Get Email</Link></li>
            <li><Link to="/register">Register</Link></li>
            <li><Link to="/login">Login</Link></li>
          </ul>
        </nav>
        <Routes> {/* Replace Switch with Routes */}
          <Route path="/" element={<ChatBox />} /> 
          <Route path="/browse_profs" element={<TextImageList />} /> 
          <Route path="/get_email" element={<EmailDisplay />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/login" element={<LoginForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
