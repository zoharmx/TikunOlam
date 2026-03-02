import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getAnalytics } from 'firebase/analytics';

// Firebase configuration from your project
const firebaseConfig = {
  apiKey: "AIzaSyAzUqzmC22jxX0__o2BXjdAAPCRE5ou1_Q",
  authDomain: "tikunframework.firebaseapp.com",
  databaseURL: "https://tikunframework-default-rtdb.firebaseio.com",
  projectId: "tikunframework",
  storageBucket: "tikunframework.firebasestorage.app",
  messagingSenderId: "495684990330",
  appId: "1:495684990330:web:f5fa0a18e302f42f5112c3",
  measurementId: "G-FJFHJ7WHN6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

// Initialize Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

// Initialize Analytics (optional)
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

export default app;
