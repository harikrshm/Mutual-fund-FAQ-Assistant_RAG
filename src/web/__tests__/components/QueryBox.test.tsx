import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import QueryBox from '../../components/QueryBox';

describe('QueryBox', () => {
  it('renders query input', () => {
    const onSubmit = jest.fn();
    render(<QueryBox onSubmit={onSubmit} />);
    
    const input = screen.getByLabelText(/query input/i);
    expect(input).toBeInTheDocument();
  });

  it('calls onSubmit when form is submitted', () => {
    const onSubmit = jest.fn();
    render(<QueryBox onSubmit={onSubmit} />);
    
    const input = screen.getByLabelText(/query input/i);
    const submitButton = screen.getByLabelText(/submit query/i);
    
    fireEvent.change(input, { target: { value: 'test query' } });
    fireEvent.click(submitButton);
    
    expect(onSubmit).toHaveBeenCalledWith('test query');
  });

  it('displays error message when error prop is provided', () => {
    const onSubmit = jest.fn();
    render(<QueryBox onSubmit={onSubmit} error="Test error" />);
    
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('disables input when disabled prop is true', () => {
    const onSubmit = jest.fn();
    render(<QueryBox onSubmit={onSubmit} disabled />);
    
    const input = screen.getByLabelText(/query input/i);
    expect(input).toBeDisabled();
  });
});

