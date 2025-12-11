import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({
  size = 'default',
  text = 'Loading...',
  showText = true,
  className = '',
  variant = 'primary'
}) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    default: 'w-8 h-8',
    large: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const variantClasses = {
    primary: 'text-accent-primary',
    secondary: 'text-text-secondary',
    white: 'text-white'
  };

  const spinnerVariants = {
    animate: {
      rotate: 360,
      transition: {
        duration: 1,
        repeat: Infinity,
        ease: "linear"
      }
    }
  };

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <motion.div
        className={`${sizeClasses[size]} ${variantClasses[variant]}`}
        variants={spinnerVariants}
        animate="animate"
      >
        <i className="fas fa-spinner fa-spin w-full h-full"></i>
      </motion.div>
      
      {showText && text && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-text-secondary text-sm"
        >
          {text}
        </motion.p>
      )}
    </div>
  );
};

export default LoadingSpinner; 
