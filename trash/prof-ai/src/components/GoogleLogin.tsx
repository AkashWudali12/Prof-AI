import React from 'react';
import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth'; // Import required methods and types
import { auth, googleProvider } from '../services/firebase';

const GoogleLogin: React.FC = () => {
  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider); // Use signInWithPopup with modular syntax
      const user = result.user;

      if (user) {
        // Redirect to additional information form or handle further steps
        console.log('User signed in:', user);
      }
    } catch (error) {
      console.error('Error signing in with Google:', error);
    }
  };

  return (
    <button onClick={handleGoogleLogin}>
      Sign in with Google
    </button>
  );
};

export default GoogleLogin;
