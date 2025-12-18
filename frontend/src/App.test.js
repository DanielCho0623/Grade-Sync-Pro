import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    // Basic smoke test - just ensure app renders
    expect(document.body).toBeInTheDocument();
  });
});
