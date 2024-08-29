import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import './styles/tailwind.css'

const RegisterForm: React.FC = () => {
  return (
    <Formik
      initialValues={{
        email: '',
        password: '',
        school: '',
        grade: '',
        major: ''
      }}
      validationSchema={Yup.object({
        email: Yup.string().email('Invalid email address').required('Required'),
        password: Yup.string().min(6, 'Must be 6 characters or more').required('Required'),
        school: Yup.string().required('Required'),
        grade: Yup.string().required('Required'),
        major: Yup.string().required('Required'),
      })}
      onSubmit={(values, { setSubmitting }) => {
        // Handle form submission
        console.log(values);
        setSubmitting(false);
      }}
    >
      <Form>
        <label htmlFor="email">Email</label>
        <Field name="email" type="email" />
        <ErrorMessage name="email" />

        <label htmlFor="password">Password</label>
        <Field name="password" type="password" />
        <ErrorMessage name="password" />

        <label htmlFor="school">School</label>
        <Field name="school" type="text" />
        <ErrorMessage name="school" />

        <label htmlFor="grade">Grade</label>
        <Field name="grade" type="text" />
        <ErrorMessage name="grade" />

        <label htmlFor="major">Major</label>
        <Field name="major" type="text" />
        <ErrorMessage name="major" />

        <button type="submit">Register</button>
      </Form>
    </Formik>
  );
};

export default RegisterForm;
