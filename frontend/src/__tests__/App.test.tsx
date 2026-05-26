import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '../store';
import App from '../App';

test('renders the app without crashing', () => {
  render(
    <Provider store={store}>
      <App />
    </Provider>
  );
  // Since user is not authenticated, it should redirect to login
  // The login page should show "Welcome Back"
  const welcomeText = screen.getByText(/welcome back/i);
  expect(welcomeText).toBeInTheDocument();
});

test('renders login form with email and password fields', () => {
  render(
    <Provider store={store}>
      <App />
    </Provider>
  );
  const emailInput = screen.getByPlaceholderText(/you@example.com/i);
  expect(emailInput).toBeInTheDocument();
  
  const passwordInput = screen.getByPlaceholderText(/enter your password/i);
  expect(passwordInput).toBeInTheDocument();
});

test('renders sign in button', () => {
  render(
    <Provider store={store}>
      <App />
    </Provider>
  );
  const signInButton = screen.getByRole('button', { name: /sign in/i });
  expect(signInButton).toBeInTheDocument();
});

test('renders link to registration page', () => {
  render(
    <Provider store={store}>
      <App />
    </Provider>
  );
  const signUpLink = screen.getByText(/sign up/i);
  expect(signUpLink).toBeInTheDocument();
  expect(signUpLink.closest('a')).toHaveAttribute('href', '/register');
});
