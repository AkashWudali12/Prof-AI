import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth'; // Import required methods and types
import { auth, googleProvider } from '../services/firebase';



const LoginForm: React.FC = () => {

    const navigate = useNavigate();

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
    <Formik
        initialValues={{
        email: '',
        password: '',
        }}
        validationSchema={Yup.object({
        email: Yup.string().email('Invalid email address').required('Required'),
        password: Yup.string().min(6, 'Must be 6 characters or more').required('Required'),
        })}
        onSubmit={(values, { setSubmitting }) => {
        // Handle form submission
        console.log(values);
        // Here you can make a POST request to your backend to authenticate the user
        setSubmitting(false);
        }}
    >
        <Form>
        <div>
            <label htmlFor="email">Email</label>
            <Field name="email" type="email" />
            <ErrorMessage name="email" />
        </div>

        <div>
            <label htmlFor="password">Password</label>
            <Field name="password" type="password" />
            <ErrorMessage name="password" />
        </div>

        <button type="submit">Login</button>
        <button type="submit" onClick={handleGoogleLogin}>Sign In With Google</button>
        </Form>
    </Formik>
    );
};

export default LoginForm;
