import React from 'react';
import { motion } from 'framer-motion';
import './SubmitButton.css';

const SubmitButton = ({
  children,
  loading = false,
  disabled = false,
  icon = 'paper-plane',
  loadingIcon = 'sync-alt',
  className = '',
  size = 'default',
  variant = 'primary',
  ...props
}) => {
  const baseClasses = `
    submit-button font-medium transition-all duration-300
    flex items-center justify-center gap-2
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `.trim();

  const sizeClasses = {
    small: 'px-4 py-2 text-sm',
    default: 'px-6 py-3 text-base',
    large: 'px-8 py-4 text-lg'
  };

  const variantClasses = {
    primary: 'bg-accent-primary text-bg-primary hover:bg-accent-primary/90',
    secondary: 'bg-bg-tertiary text-text-secondary border border-border-color hover:bg-bg-secondary',
    danger: 'bg-red-500 text-white hover:bg-red-600',
    success: 'bg-green-500 text-white hover:bg-green-600'
  };

  const buttonClasses = `
    ${baseClasses}
    ${sizeClasses[size]}
    ${variantClasses[variant]}
    ${className}
  `.trim();

  return (
    <motion.button
      type="submit"
      disabled={disabled || loading}
      className={buttonClasses}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      {...props}
    >
      <span className="flex items-center gap-2">
        {loading ? (
          <i className={`fas fa-${loadingIcon} fa-spin`}></i>
        ) : (
          <i className={`fas fa-${icon}`}></i>
        )}
        {children}
      </span>
      <div className="button-loader"></div>
    </motion.button>
  );
};

export default SubmitButton; 
