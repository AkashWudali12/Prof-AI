// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBSj989tP3TzAj_LkVl3Zu52pCFkP8U-Hc",
  authDomain: "prof-ai-3b2ad.firebaseapp.com",
  projectId: "prof-ai-3b2ad",
  storageBucket: "prof-ai-3b2ad.appspot.com",
  messagingSenderId: "579919193707",
  appId: "1:579919193707:web:da8badb0b7afb896d8b32e",
  measurementId: "G-93B8PRD65N"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase services
export const auth = getAuth(app);
export const firestore = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();
